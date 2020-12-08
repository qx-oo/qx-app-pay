from django.utils import timezone


now = timezone.now()
now_s1 = now + timezone.timedelta(seconds=1)
now_a1 = now + timezone.timedelta(days=1)
now_b1 = now - timezone.timedelta(days=1)
now_b2 = now - timezone.timedelta(days=2)
now_b3 = now - timezone.timedelta(days=3)


def get_ms(dt):
    return str(int(dt.timestamp()) * 1000)


def get_str(dt):
    return dt.strftime('%Y-%m-%d %H:%M:%S')


resp_receipt = {
    "environment": "Sandbox",
    "receipt": {
        "receipt_type": "ProductionSandbox",
        "adam_id": 0,
        "app_item_id": 0,
        "bundle_id": "cn.app.pay",
        "application_version": "1",
        "download_id": 0,
        "version_external_identifier": 0,
        "receipt_creation_date": "{} Etc/GMT".format(get_str(now)),
        "receipt_creation_date_ms": "{}".format(get_ms(now)),
        "receipt_creation_date_pst": "{} America/Los_Angeles".format(
            get_str(now)),
        "request_date": "{} Etc/GMT".format(get_str(now)),
        "request_date_ms": "{}".format(get_ms(now)),
        "request_date_pst": "{} America/Los_Angeles".format(get_str(now)),
        "original_purchase_date": "{} Etc/GMT".format(get_str(now)),
        "original_purchase_date_ms": "{}".format(get_ms(now)),
        "original_purchase_date_pst": "{} America/Los_Angeles".format(
            get_str(now)),
        "original_application_version": "1.0",
        "in_app": [
            {
                "quantity": "1",
                "product_id": "cn.app.pay.p1",
                "transaction_id": "1000000000001",
                "original_transaction_id": "1000000000001",
                "purchase_date": "{} Etc/GMT".format(get_str(now_b3)),
                "purchase_date_ms": "{}".format(get_ms(now_b3)),
                "purchase_date_pst": "{} America/Los_Angeles".format(
                    get_str(now_b3)),
                "original_purchase_date": "{} Etc/GMT".format(get_str(now_b3)),
                "original_purchase_date_ms": "{}".format(get_ms(now_b3)),
                "original_purchase_date_pst": "{} America/Los_Angeles".format(
                    get_str(now_b3)),
                "expires_date": "{} Etc/GMT".format(get_str(now_b2)),
                "expires_date_ms": "{}".format(get_ms(now_b2)),
                "expires_date_pst": "{} America/Los_Angeles".format(
                    get_str(now_b2)),
                "web_order_line_item_id": "xxxxx",
                "is_trial_period": "false",
                "is_in_intro_offer_period": "false"
            },
            {
                "quantity": "1",
                "product_id": "cn.app.pay.p2",
                "transaction_id": "1000000000002",
                "original_transaction_id": "1000000000002",
                "purchase_date": "{} Etc/GMT".format(get_str(now_s1)),
                "purchase_date_ms": "{}".format(get_ms(now_s1)),
                "purchase_date_pst": "{} America/Los_Angeles".format(
                    get_str(now_s1)),
                "original_purchase_date": "{} Etc/GMT".format(get_str(now_s1)),
                "original_purchase_date_ms": "{}".format(get_ms(now_s1)),
                "original_purchase_date_pst": "{} America/Los_Angeles".format(
                    get_str(now_s1)),
                "expires_date": "{} Etc/GMT".format(
                    get_str(now_s1 + timezone.timedelta(minutes=5))),
                "expires_date_ms": "{}".format(
                    get_ms(now_s1 + timezone.timedelta(minutes=5))),
                "expires_date_pst": "{} America/Los_Angeles".format(
                    get_str(now_s1 + timezone.timedelta(minutes=5))),
                "web_order_line_item_id": "xxxxxxx",
                "is_trial_period": "false",
                "is_in_intro_offer_period": "false"
            },
            {
                "quantity": "1",
                "product_id": "cn.app.pay.p1",
                "transaction_id": "10000000000012",
                "original_transaction_id": "1000000000001",
                "purchase_date": "{} Etc/GMT".format(get_str(now_b2)),
                "purchase_date_ms": "{}".format(get_ms(now_b2)),
                "purchase_date_pst": "{} America/Los_Angeles".format(
                    get_str(now_b2)),
                "original_purchase_date": "{} Etc/GMT".format(get_str(now_b2)),
                "original_purchase_date_ms": "{}".format(get_ms(now_b2)),
                "original_purchase_date_pst": "{} America/Los_Angeles".format(
                    get_str(now_b2)),
                "expires_date": "{} Etc/GMT".format(get_str(now_b1)),
                "expires_date_ms": "{}".format(get_ms(now_b1)),
                "expires_date_pst": "{} America/Los_Angeles".format(
                    get_str(now_b1)),
                "web_order_line_item_id": "xxxxx",
                "is_trial_period": "false",
                "is_in_intro_offer_period": "false"
            },
            {
                "quantity": "1",
                "product_id": "cn.app.pay.p1",
                "transaction_id": "10000000000013",
                "original_transaction_id": "1000000000001",
                "purchase_date": "{} Etc/GMT".format(get_str(now_b1)),
                "purchase_date_ms": "{}".format(get_ms(now_b1)),
                "purchase_date_pst": "{} America/Los_Angeles".format(
                    get_str(now_b1)),
                "original_purchase_date": "{} Etc/GMT".format(get_str(now_b1)),
                "original_purchase_date_ms": "{}".format(get_ms(now_b1)),
                "original_purchase_date_pst": "{} America/Los_Angeles".format(
                    get_str(now_b1)),
                "expires_date": "{} Etc/GMT".format(get_str(now)),
                "expires_date_ms": "{}".format(get_ms(now)),
                "expires_date_pst": "{} America/Los_Angeles".format(
                    get_str(now)),
                "web_order_line_item_id": "xxxxx",
                "is_trial_period": "false",
                "is_in_intro_offer_period": "false"
            }
        ]
    },
    "latest_receipt_info": [
        {
            "quantity": "1",
            "product_id": "cn.app.pay.p1",
            "transaction_id": "10000000000012",
            "original_transaction_id": "1000000000001",
            "purchase_date": "{} Etc/GMT".format(get_str(now_b2)),
            "purchase_date_ms": "{}".format(get_ms(now_b2)),
            "purchase_date_pst": "{} America/Los_Angeles".format(
                get_str(now_b2)),
            "original_purchase_date": "{} Etc/GMT".format(get_str(now_b2)),
            "original_purchase_date_ms": "{}".format(get_ms(now_b2)),
            "original_purchase_date_pst": "{} America/Los_Angeles".format(
                get_str(now_b2)),
            "expires_date": "{} Etc/GMT".format(get_str(now_b1)),
            "expires_date_ms": "{}".format(get_ms(now_b1)),
            "expires_date_pst": "{} America/Los_Angeles".format(
                get_str(now_b1)),
            "web_order_line_item_id": "xxxxx",
            "is_trial_period": "false",
            "is_in_intro_offer_period": "false"
        },
        {
            "quantity": "1",
            "product_id": "cn.app.pay.p1",
            "transaction_id": "10000000000013",
            "original_transaction_id": "1000000000001",
            "purchase_date": "{} Etc/GMT".format(get_str(now_b1)),
            "purchase_date_ms": "{}".format(get_ms(now_b1)),
            "purchase_date_pst": "{} America/Los_Angeles".format(
                get_str(now_b1)),
            "original_purchase_date": "{} Etc/GMT".format(
                get_str(now_b1)),
            "original_purchase_date_ms": "{}".format(get_ms(now_b1)),
            "original_purchase_date_pst": "{} America/Los_Angeles".format(
                get_str(now_b1)),
            "expires_date": "{} Etc/GMT".format(get_str(now)),
            "expires_date_ms": "{}".format(get_ms(now)),
            "expires_date_pst": "{} America/Los_Angeles".format(get_str(now)),
            "web_order_line_item_id": "xxxxx",
            "is_trial_period": "false",
            "is_in_intro_offer_period": "false"
        },
        {
            "quantity": "1",
            "product_id": "cn.app.pay.p1",
            "transaction_id": "10000000000014",
            "original_transaction_id": "1000000000001",
            "purchase_date": "{} Etc/GMT".format(get_str(now)),
            "purchase_date_ms": "{}".format(get_ms(now)),
            "purchase_date_pst": "{} America/Los_Angeles".format(get_str(now)),
            "original_purchase_date": "{} Etc/GMT".format(get_str(now)),
            "original_purchase_date_ms": "{}".format(get_ms(now)),
            "original_purchase_date_pst": "{} America/Los_Angeles".format(
                get_str(now)),
            "expires_date": "{} Etc/GMT".format(get_str(now_a1)),
            "expires_date_ms": "{}".format(get_ms(now_a1)),
            "expires_date_pst": "{} America/Los_Angeles".format(
                get_str(now_a1)),
            "web_order_line_item_id": "xxxxx",
            "is_trial_period": "false",
            "is_in_intro_offer_period": "false"
        }
    ],
    "latest_receipt": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  # noqa
    "pending_renewal_info": [
        {
            "expiration_intent": "1",
            "auto_renew_product_id": "cn.app.pay.p1",
            "original_transaction_id": "1000000000001",
            "is_in_billing_retry_period": "0",
            "product_id": "cn.app.pay.p1",
            "auto_renew_status": "1"
        },
        {
            "expiration_intent": "1",
            "auto_renew_product_id": "cn.app.pay.p2",
            "original_transaction_id": "1000000000002",
            "is_in_billing_retry_period": "0",
            "product_id": "cn.app.pay.p2",
            "auto_renew_status": "0"
        }
    ],
    "status": 0
}


req_s2s = {
    "latest_receipt": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  # noqa
    "latest_receipt_info": {
        "original_purchase_date_pst": "{} America/Los_Angeles".format(
            get_str(now)),
        "quantity": "1",
        "unique_vendor_identifier": "XXX",
        "original_purchase_date_ms": "{}".format(get_ms(now)),
        "expires_date_formatted": "{} Etc/GMT".format(get_str(now_a1)),
        "is_in_intro_offer_period": "false",
        "purchase_date_ms": "{}".format(get_ms(now)),
        "expires_date_formatted_pst": "{} America/Los_Angeles".format(
            get_str(now_a1)),
        "is_trial_period": "true",
        "item_id": "111111",
        "unique_identifier": "00000",
        "original_transaction_id": "1000000000001",
        "expires_date": "00000000",
        "app_item_id": "0000000",
        "transaction_id": "10000000000014",
        "bvrs": "00000",
        "web_order_line_item_id": "00000000",
        "version_external_identifier": "000000",
        "bid": "cn.app.pay",
        "product_id": "cn.app.pay.p1",
        "purchase_date": "2019-07-30 04:13:17 Etc/GMT",
        "purchase_date_pst": "2019-07-29 21:13:17 America/Los_Angeles",
        "original_purchase_date": "2019-07-30 04:13:18 Etc/GMT"
    },
    "environment": "PROD",
    "auto_renew_status": "true",
    "password": "test_password",
    "auto_renew_product_id": "cn.app.pay.p1",
    "notification_type": "DID_RENEW"
}


class Resp():

    def json(self):
        return resp_receipt
