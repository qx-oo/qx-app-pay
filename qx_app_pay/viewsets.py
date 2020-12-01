from rest_framework.permissions import (
    AllowAny, IsAuthenticated,
)
from django.utils import timezone
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from .apple_pay import ApplePay
from .models import AppReceipt, AppOrder


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
        # order_no = AppReceipt.get_apple_order_no(
        #     bid, product_id, purchase_date_ms, '')
        order = AppOrder.objects.filter(
            related_id=transaction_id, category='apple_store').first()
        if order and order.payment_type == 'appreceipt':
            payment = AppReceipt.objects.filter(id=order.payment_id).first()
            payment.last_subscription_info = data
            last_update_time = timezone.datetime.fromtimestamp(
                int(purchase_date_ms) // 1000)
            payment.last_update_time = last_update_time
    return JsonResponse(data={}, status=200)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def apple_subscription(request):
    """
    """
    pass
