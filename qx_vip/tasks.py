import logging
from django.utils import timezone
from django.db.models import Q, F
from qx_app_pay.models import AppReceipt
from qx_app_pay.utils import apple_subscription_update
from .models import ConsumeDayLog


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


class ConsumeDaysVipTask():
    """
    Every Day Consume User Vip days
    """
    userinfo_model = None

    def run(self):
        if model := self.userinfo_model:
            date = timezone.localtime(timezone.now()).date()
            if ConsumeDayLog.objects.filter(date=date).exists():
                logger.error("Already Consume User Vip day")
                return

            ids = list(model.objects.filter(
                Q(vip_expire_date=None) | Q(vip_expire_date__lt=date),
                available_days__gt=0).values_list('user_id', flat=True))

            step = 5000
            for index in range(len(ids) // step + 1):
                _ids = ids[index * step: (index + 1) * step]
                model.objects.filter(
                    user_id__in=_ids).update(
                        available_days=F('available_days') - 1)
                ConsumeDayLog.objects.create(
                    date=date, info={'ids': ids})
        else:
            raise NotImplementedError('userinfo_model is None')
