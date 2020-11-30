from django.conf import settings


QX_APP_PAY_SETTINGS = {
    "APPLE_PAY": {
        "PASSWORD": None,
    },
}

app_pay_settings = getattr(
    settings, 'QX_APP_PAY_SETTINGS',
    QX_APP_PAY_SETTINGS)
