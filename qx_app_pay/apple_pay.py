from .models import AppProduct


class ApplePay():

    def __init__(self, kwargs={}):
        params = {'password', }
        if require := (params - set(kwargs.keys())):
            raise TypeError("{} is required".format(require))
        pass

    def validate(self, b64_receipt):
        receipt_json = {
            "receipt-data": receipt,
            "password": '',
        }
