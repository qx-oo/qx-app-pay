import logging
from rest_framework.permissions import (
    AllowAny, IsAuthenticated,
)
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
try:
    from drf_yasg.utils import swagger_auto_schema
except ImportError:
    def func_none(*args, **kwargs):
        def _func(func):
            def _func2(*f_args, **f_kwargs):
                return func(*f_args, **f_kwargs)
            return _func2
        return _func
    swagger_auto_schema = func_none
from .serializers import AppleSubscription
from .utils import (
    apple_subscription_update,
    apple_subscription_notification,
    VerifyException, PaymentException
)


logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes((AllowAny,))
def apple_notifications(request) -> JsonResponse:
    """
    Apple server to server notifications

    recieve apple notifications
    """
    data = request.data
    apple_subscription_notification(data)
    return JsonResponse(data={}, status=200)


@swagger_auto_schema(
    methods=['post'], request_body=AppleSubscription,
    responses={200: {}})
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
        status, msg = apple_subscription_update(
            req_data['b64_receipt'], request.user.id)
        if not status:
            return JsonResponse(data={
                "code": 4000,
                "msg": [msg],
            }, status=200)
    except VerifyException:
        return JsonResponse(data={
            "code": 4014,
            "msg": ["Verify Fail"],
        }, status=200)
    except PaymentException:
        return JsonResponse(data={
            "code": 4000,
            "msg": ["Save Fail"],
        }, status=200)
    return JsonResponse(data={
        "code": 200,
        "msg": ["success"],
        "data": {},
    }, status=200)
