import typing
import logging
from django.utils import timezone
from django.utils.module_loading import import_string
from .settings import app_pay_settings
from .apple_pay import ApplePay
from .models import AppReceipt, AppOrder


logger = logging.getLogger(__name__)


RECEIPT_ORDERS_CALLBACK = import_string(
    app_pay_settings['RECEIPT_ORDERS_CALLBACK'])
NOTIFICATION_CALLBACK = import_string(
    app_pay_settings['NOTIFICATION_CALLBACK'])


class VerifyException(Exception):
    pass


class PaymentException(Exception):
    pass


def apple_subscription_update(b64_receipt, user_id) -> typing.Tuple[bool, str]:
    """
    update apple subscription status
    RECEIPT_ORDERS_CALLBACK(user_id: int, orders: [], renew_status: {}) -> bool
    return: status, msg
    """
    try:
        status, data = ApplePay().validate_receipt(b64_receipt)
        if status != 0:
            return False, data
    except Exception:
        logger.exception("apple_verify_receipt")
        raise VerifyException
    try:
        AppReceipt.save_payment(
            'apple_store', user_id, data,
            RECEIPT_ORDERS_CALLBACK)
    except Exception:
        logger.exception("apple_save_payment")
        raise PaymentException
    return True, ''


def apple_subscription_notification(data):
    """
    NOTIFICATION_CALLBACK(user_id, data)
    """

    status, ret = ApplePay().parse_subscription(data)
    if status:
        # bid, product_id, purchase_date_ms, transaction_id = ret
        order = AppOrder.objects.filter(
            related_id=ret['receipt_info']['transaction_id'],
            product__category='apple_store').first()
        if order and order.payment_type == 'appreceipt':
            payment = AppReceipt.objects.filter(
                id=order.payment_id, user_id=order.user_id).first()
            payment.update_info['last_update'] = data
            payment.update_info.setdefault('history', []).append({
                'prodcut_id': ret['prodcut_id'],
                'type': ret['notification_type'],
            })
            last_update_time = timezone.datetime.fromtimestamp(
                int(ret['receipt_info']['purchase_date_ms']) // 1000,
                tz=timezone.utc)
            payment.last_update_time = last_update_time
            payment.save()
            NOTIFICATION_CALLBACK(order.user_id, ret)
