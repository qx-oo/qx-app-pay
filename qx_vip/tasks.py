import logging
from django.utils import timezone
from qx_app_pay.models import AppReceipt
from qx_app_pay.utils import apple_subscription_update


logger = logging.getLogger(__name__)


class UpdateVipReceiptTask():
    """
    Every Day Check Vip User Apple Receipt
    _type: 1(today), 2(yesterday)
    """
    userinfo_model = None

    def run(self, _type=1):
        if model := self.userinfo_model:
            if _type == 1:
                date = timezone.localtime(timezone.now()).date()
            else:
                date = timezone.localtime(
                    timezone.now() - timezone.timedelta(days=1)).date()
            for userinfo in model.objects.filter(
                    vip_expire_date=date):
                try:
                    if receipt := AppReceipt.objects.filter(
                            user_id=userinfo.user_id,
                            category='apple_store').first():
                        apple_subscription_update(
                            receipt.b64_receipt, receipt.user_id)
                except Exception:
                    logger.exception("UpdateVipReceiptTask")
        else:
            raise NotImplementedError('userinfo_model is None')
