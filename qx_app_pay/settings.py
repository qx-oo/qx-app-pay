from django.conf import settings
from django.utils.module_loading import import_string


QX_APP_PAY_SETTINGS = {
    "APPLE_PAY": {
        "PASSWORD": None,
    },
    "RECEIPT_ORDER_OBJECT_CALLBACK": None,
}

app_pay_settings = getattr(
    settings, 'QX_APP_PAY_SETTINGS',
    QX_APP_PAY_SETTINGS)
app_pay_settings['RECEIPT_ORDER_OBJECT_CALLBACK'] = import_string(
    app_pay_settings['RECEIPT_ORDER_OBJECT_CALLBACK'])
