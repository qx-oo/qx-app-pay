from qx_test.members.models import UserInfo


def orders_callback(*args, **kwargs):
    return UserInfo.orders_callback(*args, **kwargs)


def notification_callback(*args, **kwargs):
    return UserInfo.notification_callback(*args, **kwargs)
