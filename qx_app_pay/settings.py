from django.conf import settings


QX_APP_PAY_SETTINGS = {
    "APPLE_PAY": {
        "PASSWORD": None,
    },
    "RECEIPT_ORDERS_CALLBACK": None,
    "APPLE_VIP_PRODUCT_ID": None,
}

app_pay_settings = getattr(
    settings, 'QX_APP_PAY_SETTINGS',
    QX_APP_PAY_SETTINGS)
