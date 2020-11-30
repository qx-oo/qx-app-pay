from rest_framework.permissions import (
    AllowAny, IsAuthenticated,
)
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from .apple_pay import ApplePay
from .models import AppReceipt


@api_view(['POST'])
@permission_classes((AllowAny,))
def apple_notifications(request) -> JsonResponse:
    """
    Apple server to server notifications

    recieve apple notifications
    """
    data = request.data
    status, _, p_id, _ = ApplePay().parse_subscription(data)
    if status:
        pass
    return JsonResponse(data={}, status=200)
