from django.db import models
from django.utils import timezone
from qx_app_pay.settings import app_pay_settings


apple_vip_product_id = app_pay_settings['APPLE_VIP_PRODUCT_ID']


class VipUserInfo(models.Model):
    """
    One To One User
    """

    vip_expire_date = models.DateField(
        verbose_name="Expire Date", default=None, null=True)
    is_trial = models.BooleanField(
        verbose_name="Is Trial", default=False)
    available_days = models.PositiveIntegerField(
        verbose_name="Available Days", default=0)
    apple_auto_renew = models.BooleanField(
        verbose_name="Apple Is Auto Renew Subscription", default=False)
    vip_order = models.JSONField(
        verbose_name="Vip Orders", default=dict)

    @staticmethod
    def user_is_vip(expire_date, available_days: int):
        if isinstance(expire_date, str):
            expire_date = timezone.datetime.strptime(
                expire_date, "%Y-%m-%d").date()
        today = timezone.localtime(timezone.now()).date()
        if today <= expire_date or available_days:
            return True
        return False

    def is_vip(self):
        return self.user_is_vip(
            self.vip_expire_date, self.available_days)

    @classmethod
    def orders_callback(cls, user_id, orders, auto_renew):
        if not orders:
            return False
        userinfo = cls.objects.filter(user_id=user_id).first()
        if not userinfo:
            return False
        used_ids = userinfo.vip_order.get('used_ids', [])
        for order in orders:
            if order.id in used_ids:
                continue
            if order.product.product_id == apple_vip_product_id:
                _type = order.extra_info.get('type')
                is_trial = order.extra_info.get('is_trial', False)
                userinfo.apple_auto_renew = auto_renew.get(
                    apple_vip_product_id, False)
                # every body trial once
                if userinfo.is_trial and is_trial:
                    continue
                if _type == 'subscription':
                    if expires_date := order.extra_info.get('expires_date'):
                        expires_date = timezone.datetime.strptime(
                            expires_date, "%Y-%m-%d").date()
                        if not userinfo.vip_expire_date or \
                                userinfo.vip_expire_date < expires_date:
                            userinfo.vip_expire_date = expires_date
                    used_ids.append(order.id)
            else:
                continue
        userinfo.vip_order['used_ids'] = used_ids
        userinfo.save()
        return True

    class Meta:
        abstract = True
        verbose_name = 'UserInfo'
        verbose_name_plural = verbose_name
