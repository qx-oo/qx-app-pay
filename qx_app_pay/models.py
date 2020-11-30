from django.db import models, transaction
from django.utils import timezone
from djang.apps import apps


PAY_PLATFORM = [
    ('apple_store', 'Apple Store',),
]


class AppProduct(models.Model):

    identifier = models.CharField(
        verbose_name="Product Identifier", max_length=250)
    name = models.CharField(
        verbose_name="Product Name", max_length=255)
    desc = models.CharField(
        verbose_name="Desc", max_length=255)
    price = models.DecimalField(
        verbose_name="Price",
        max_digits=8, decimal_places=2,
        default=0,
    )
    currency = models.CharField(
        verbose_name='Currency', max_lenght=10)
    category = models.CharField(
        verbose_name="Platform", max_length=32,
        choices=PAY_PLATFORM
    )

    class Meta:
        verbose_name = "AppProduct"
        verbose_name_plural = verbose_name
        unique_together = (('category', 'identifier'),)


class AppReceipt(models.Model):

    user_id = models.IntegerField(
        verbose_name="User Id", db_index=True)
    b64_receipt = models.TextField(
        verbose_name="Base64 Query Receipt", null=True)
    detail = models.JSONField(
        verbose_name="Detail")
    product = models.ForeignKey(
        AppProduct, verbose_name="Product", on_delete=models.PROTECT)
    created = models.DateTimeField(
        verbose_name='Created', default=timezone.now, editable=False)
    last_update_time = models.DateTimeField(
        verbose_name='Last Update Time', default=timezone.now)
    last_subscription_info = models.JSONField(
        verbose_name="Subscription Info", default=dict)

    @classmethod
    def save_payment(cls, bundle_id, user_id: int, receipt: dict,
                     object_type: str, object_id=None):
        """
        Save Receipt And Create Order
        """
        AppOrder = apps.get_model('qx_app_pay.AppOrder')
        with transaction.atomic():
            product = AppProduct.objects.get(identifier=bundle_id)
            if product.category == 'apple_store':
                b64receipt = receipt['latest_receipt']
                instance, created = cls.objects.get_or_create(
                    user_id=user_id, product=product,
                    defaults={'b64_receipt': b64receipt, 'detail': receipt}
                )
                if not created:
                    instance.b64_receipt = b64receipt
                    instance.detail = receipt
                    instance.save()
                order_list = {}
                receipt_list = list(receipt['latest_receipt_info'])
                receipt_list.extend(receipt['receipt']['in_app'])
                for item in receipt_list:
                    order_no, receipt, price, pay_ts = instance.get_order_info(
                        bundle_id, item)
                    pay_time = timezone.datetime.fromtimestamp(pay_ts)
                    order_list[order_no] = {
                        "order_no": order_no,
                        "user_id": user_id,
                        "currency": product.currency,
                        "amount": price,
                        "category": product.category,
                        "payment_id": instance.id,
                        "payment_type": "appreceipt",
                        "object_id": object_id,
                        "object_type": object_type,
                        "extra_info": item,
                        "pay_time": pay_time,
                    }
                _exists = AppOrder.objects.filter(order_no__in=list(
                    order_list.keys())).values_list('order_no', flat=True)
                orders = [order for no, order in order_list.items()
                          if no not in _exists]
                AppOrder.objects.bulk_create(orders)
            else:
                raise TypeError

    @classmethod
    def get_order_no(cls, bundle_id, product_id, purchase_date_ms):
        purchase_date_ts = purchase_date_ms // 1000
        return "{}-{}-{}".format(
            bundle_id, product_id, purchase_date_ts)

    def get_order_info(self, bundle_id, receipt: dict) -> (str, dict, float):
        """
        Get receipt's order info
        """
        price = self.product.price
        if self.product.category == 'apple_store':
            purchase_date_ts = int(receipt['purchase_date_ms']) // 1000
            product_id = receipt['product_id']
            order_no = self.get_order_no(
                bundle_id, receipt['product_id'], receipt['purchase_date_ms'])
            order_no = "{}-{}-{}".format(
                bundle_id, product_id, purchase_date_ts)
        else:
            raise TypeError
        return order_no, receipt, price, purchase_date_ts

    class Meta:
        verbose_name = "AppReceipt"
        verbose_name_plural = verbose_name
        unique_together = (('user_id', 'product'),)


class AppOrder(models.Model):

    order_no = models.CharField(
        verbose_name='App Order Unique Id', unique=True, max_length=250)
    user_id = models.IntegerField(
        verbose_name="User Id", db_index=True)
    object_id = models.IntegerField(
        verbose_name="Ojbect Id", null=True, blank=True)
    object_type = models.CharField(
        verbose_name="Object Type", max_length=50)
    created = models.DateTimeField(
        verbose_name='Created', default=timezone.now, editable=False)
    category = models.CharField(
        verbose_name="Platform", max_length=32,
        choices=PAY_PLATFORM,
    )
    pay_time = models.DateTimeField(
        verbose_name="Pay Time")
    amount = models.DecimalField(
        verbose_name="Amount",
        max_digits=8, decimal_places=2,
        default=0,
    )
    currency = models.CharField(
        verbose_name='Currency', max_lenght=10)
    extra_info = models.JSONField(
        verbose_name="Extra Info", default=dict)
    payment_id = models.IntegerField(
        verbose_name="Payment id")
    payment_type = models.CharField(
        verbose_name="Payment Type", max_length=32,
        choices=[
            ('appreceipt', 'AppReceipt',),
        ]
    )
    refund = models.BooleanField(
        verbose_name="Is Refund", default=False)

    class Meta:
        verbose_name = "AppOrder"
        verbose_name_plural = verbose_name
