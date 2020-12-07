from qx_vip.tasks import UpdateVipReceiptTask, ConsumeDaysVipTask
from .models import UserInfo


class MyUpdateVipReceiptTask(UpdateVipReceiptTask):

    userinfo_model = UserInfo


class MyConsumeDaysVipTask(ConsumeDaysVipTask):

    userinfo_model = UserInfo
