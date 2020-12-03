import logging
from rest_framework.permissions import (
    AllowAny, IsAuthenticated,
)
from django.utils import timezone
from django.http import JsonResponse
from django.utils.module_loading import import_string
from rest_framework.decorators import api_view, permission_classes
from .apple_pay import ApplePay
from .models import AppReceipt, AppOrder
from .serializers import AppleSubscription
from .settings import app_pay_settings


logger = logging.getLogger(__name__)

RECEIPT_ORDERS_CALLBACK = import_string(
    app_pay_settings['RECEIPT_ORDERS_CALLBACK'])


@api_view(['POST'])
@permission_classes((AllowAny,))
def apple_notifications(request) -> JsonResponse:
    """
    Apple server to server notifications

    recieve apple notifications
    """
    data = request.data
    status, ret = ApplePay().parse_subscription(data)
    if status:
        bid, product_id, purchase_date_ms, transaction_id = ret
        order = AppOrder.objects.filter(
            related_id=transaction_id, category='apple_store').first()
        if order and order.payment_type == 'appreceipt':
            payment = AppReceipt.objects.filter(id=order.payment_id).first()
            payment.last_subscription_info = data
            last_update_time = timezone.datetime.fromtimestamp(
                int(purchase_date_ms) // 1000, tz=timezone.utc)
            payment.last_update_time = last_update_time
    return JsonResponse(data={}, status=200)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def apple_subscription(request):
    """
    Apple Store Subscription

    request: {"b64_receipt": "..."}
    """
    serializer = AppleSubscription(data=request.data)
    serializer.is_valid(raise_exception=True)
    req_data = serializer.data
    try:
        status, data = ApplePay().validate_receipt(req_data['b64_receipt'])
        if status != 0:
            return JsonResponse(data={
                "code": 4000,
                "msg": [data],
            }, status=200)
    except Exception:
        logger.error("apple_subscription")
        return JsonResponse(data={
            "code": 4014,
            "msg": ["Verify Fail"],
        }, status=200)
    try:
        AppReceipt.save_payment(
            'apple_store', request.user.id, data,
            RECEIPT_ORDERS_CALLBACK)
    except Exception:
        logger.error("apple_save_payment")
        return JsonResponse(data={
            "code": 4000,
            "msg": ["Save Fail"],
        }, status=200)
    return JsonResponse(data={
        "code": 200,
        "msg": ["success"],
        "data": {},
    }, status=200)
