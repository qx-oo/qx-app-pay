from qx_vip.tasks import UpdateVipReceiptTask
from .models import UserInfo


class MyUpdateVipReceiptTask(UpdateVipReceiptTask):

    userinfo_model = UserInfo
