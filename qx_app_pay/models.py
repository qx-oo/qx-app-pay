from django.db import models
from django.utils import timezone


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
    category = models.CharField(
        verbose_name="Platform", max_length=32,
        choices=PAY_PLATFORM
    )

    class Meta:
        verbose_name = "AppProduct"
        verbose_name_plural = verbose_name


class AppReceipt(models.Model):

    user_id = models.IntegerField(
        verbose_name="User Id", db_index=True)
    b64_receipt = models.TextField(
        verbose_name="Base64 Query Receipt", null=True)
    detail = models.JSONField(
        verbose_name="Detail")
    category = models.CharField(
        verbose_name="Platform", max_length=32,
        choices=PAY_PLATFORM
    )
    product_id = models.IntegerField(
        verbose_name="Product id")
    created = models.DateTimeField(
        verbose_name='Created', default=timezone.now, editable=False)

    class Meta:
        verbose_name = "AppReceipt"
        verbose_name_plural = verbose_name
        unique_together = (('user_id', 'category', 'product_id'),)


class PayOrder(models.Model):

    order_no = models.CharField(
        verbose_name='App Order Unique Id', unique=True)
    user_id = models.IntegerField(
        verbose_name="User Id", db_index=True)
    object_id = models.IntegerField(
        verbose_name="Ojbect Id", null=True, blank=True)
    created = models.DateTimeField(
        verbose_name='Created', default=timezone.now, editable=False)
    category = models.CharField(
        verbose_name="Platform", max_length=32,
        choices=[
            ('apple_store', 'Apple Store',),
        ]
    )
    pay_date = models.DateField(
        verbose_name="Pay Date")
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

    class Meta:
        verbose_name = "PayOrder"
        verbose_name_plural = verbose_name