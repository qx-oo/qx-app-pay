# qx-app-pay

my django project app pay

### Install:

    pip install -e git://github.com/qx-oo/qx-app-pay.git@master#egg=qx-app-pay

### Usage:

settings.py:

    INSTALLED_APPS = [
        ...
        'qx_app_pay',
        'qx_vip',
        ...
    ]

    QX_APP_PAY_SETTINGS = {
        "APPLE_PAY": {
            "PASSWORD": '...',
        },
        "RECEIPT_ORDERS_CALLBACK": "qx_test.members.utils.orders_callback",
        "NOTIFICATION_CALLBACK": "qx_test.members.utils.notification_callback",
        "APPLE_VIP_PRODUCT_ID": "cn....",
    }

models.py:

    class UserInfo(..., VipUserInfo):
        ...

    def orders_callback(*args, **kwargs):
        return UserInfo.orders_callback(*args, **kwargs)

    def notification_callback(*args, **kwargs):
        return UserInfo.notification_callback(*args, **kwargs)

urls.py:

    urlpatterns = [
        path('apple-pay/subscription/', apple_subscription),
        path('apple-pay/notifications/', apple_notifications),
    ]