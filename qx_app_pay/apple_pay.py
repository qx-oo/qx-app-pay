import logging
import requests
import json
from .settings import app_pay_settings

logger = logging.getLogger(__name__)


class ApplePay():
    """
    Apple Pay
    """

    sanbox_url = 'https://sandbox.itunes.apple.com/{}'
    url = 'https://buy.itunes.apple.com/{}'

    def __init__(self):
        if password := app_pay_settings['APPLE_PAY']['PASSWORD']:
            self.password = password
        else:
            raise TypeError("APPLE_PAY PASSWORD is required")

    def validate_receipt(self, b64_receipt):
        """
        Verify Receipt
        try:
            ret = ApplePay().validate_receipt('xxxx')
        except TypeError as e:
            print("error: {}".format(e))
        """
        request_json = {
            "receipt-data": b64_receipt,
            "password": self.password,
        }
        data, msg = self.request('POST', 'verifyReceipt', request_json)
        if not data:
            raise TypeError(msg)
        if not data.get('status'):
            return 0, data
        status, msg = self.parse_status(data)
        return status, msg

    def request(self, method, resource, params) -> (dict, str):
        url = self.url.format(resource)
        sanbox_url = self.sanbox_url.format(resource)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        try:
            if method.upper() == 'GET':
                resp = requests.request(
                    method, url, params=params, timeout=60).json()
                if resp.get("status") in [21007, 21008]:
                    resp = requests.request(
                        method, sanbox_url, params=params, timeout=60).json()
            else:
                data = json.dumps(params)
                resp = requests.request(
                    method, url, data=data, headers=headers,
                    timeout=60).json()
                if resp.get("status") in [21007, 21008]:
                    resp = requests.request(
                        method, sanbox_url, data=data, headers=headers,
                        timeout=60).json()
            return resp, 'success'
        except Exception:
            return None, 'Http Error'

    def parse_status(self, resp):
        status = resp.get('status')
        error = {
            21000: "Bad json",
            21002: "Bad data",
            21003: "Receipt authentication",
            21004: "Shared secret mismatch",
            21005: "Server is unavailable",
            21006: "Subscription has expired",
        }
        msg = error.get(status, 'unknown')
        if msg == 'unknown':
            logger.warning("{} request error {}".format(
                self.__class__.__name__, resp))
        return status, msg

    def parse_subscription(self, data):
        """
        Parse Subscription Notification
        return: status, bid, product_id, purchase_date_ms
        """
        if self.password != data.get('password'):
            return False, None
        if receipt_info := data.get('latest_receipt_info'):
            bid = receipt_info['bid']
            product_id = receipt_info['product_id']
            purchase_date_ms = receipt_info['purchase_date_ms']
            transaction_id = receipt_info['original_transaction_id']
            return True, (bid, product_id, purchase_date_ms, transaction_id)
        return False, None
