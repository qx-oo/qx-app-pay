from django.db import models
from django.conf import settings
from qx_vip.models import VipUserInfo

# Create your models here.


class AbstractUserInfo(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True,
        verbose_name="用户")
    age = models.IntegerField(
        verbose_name="年龄", default=28)

    class Meta:
        abstract = True
        verbose_name = 'UserInfo'
        verbose_name_plural = verbose_name


class UserInfo(AbstractUserInfo, VipUserInfo):
    """
    User info
    """

    class Meta:
        verbose_name = 'UserInfo'
        verbose_name_plural = verbose_name
