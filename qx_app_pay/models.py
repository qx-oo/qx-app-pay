import logging
from django.db import models, transaction
from django.utils import timezone
from django.apps import apps


logger = logging.getLogger(__name__)


PAY_PLATFORM = [
    ('apple_store', 'Apple Store',),
]


class AppProduct(models.Model):

    product_id = models.CharField(
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
    discount = models.DecimalField(
        verbose_name="Price",
        max_digits=3, decimal_places=2,
        null=True, default=None,
    )
    currency = models.CharField(
        verbose_name='Currency', max_length=10, default='')
    category = models.CharField(
        verbose_name="Platform", max_length=32,
        choices=PAY_PLATFORM
    )
    is_active = models.BooleanField(
        verbose_name="Is Active", default=True)

    class Meta:
        verbose_name = "AppProduct"
        verbose_name_plural = verbose_name
        unique_together = (('category', 'product_id'),)


class AppReceipt(models.Model):

    user_id = models.IntegerField(
        verbose_name="User Id", db_index=True)
    b64_receipt = models.TextField(
        verbose_name="Base64 Query Receipt", null=True)
    detail = models.JSONField(
        verbose_name="Detail")
    created = models.DateTimeField(
        verbose_name='Created', default=timezone.now, editable=False)
    last_update_time = models.DateTimeField(
        verbose_name='Last Update Time', default=timezone.now)
    update_info = models.JSONField(
        verbose_name="Subscription Server 2 Server Info", default=dict)
    category = models.CharField(
        verbose_name="Platform", max_length=32,
        choices=PAY_PLATFORM
    )

    @classmethod
    def save_payment(cls, category, user_id: int, receipt: dict,
                     orders_callback=None):
        """
        Save Receipt And Create Order
        orders_callback:
            orders_callback(user_id: int, orders: [], renew_status: {}) -> bool
        """  # noqa
        AppOrder = apps.get_model('qx_app_pay.AppOrder')
        with transaction.atomic():
            if category == 'apple_store':
                payment_type = 'appreceipt'
                instance, order_list, renew_status = cls.apple_save_payment(
                    category, user_id, receipt, payment_type)
            else:
                raise TypeError
            exist_order = AppOrder.objects.filter(order_no__in=list(
                order_list.keys()))
            _exists = []
            update_order = []
            for e_order in list(exist_order):
                _exists.append(e_order.order_no)
                if order := order_list.get(e_order.order_no):
                    if order['extra_info']['expires_date'] != \
                            e_order.extra_info['expires_date']:
                        update_order.append(order)
            orders = [AppOrder(**order) for no, order in order_list.items()
                      if no not in _exists]
            # create new order
            AppOrder.objects.bulk_create(orders)
            # update change order
            for u_order in update_order:
                AppReceipt.objects.filter(
                    order_no=u_order['order_no']).update(**u_order)
        try:
            if order_list:
                _orders = list(AppOrder.objects.filter(
                    order_no__in=list(order_list.keys())))
                orders_callback(user_id, _orders, renew_status)
        except Exception:
            logger.exception('app pay object_callback')

    @classmethod
    def apple_save_payment(cls, category, user_id, receipt, payment_type):
        """
        Parse receipt and return order list
        """  # noqa
        b64receipt = receipt['latest_receipt']
        renew_status = receipt['pending_renewal_info']
        renew_status = {
            item['auto_renew_product_id']: True if int(
                item['auto_renew_status']) else False
            for item in renew_status
        }
        instance, created = cls.objects.get_or_create(
            user_id=user_id, category=category,
            defaults={'b64_receipt': b64receipt, 'detail': receipt}
        )
        order_list = {}
        receipt_list = list(receipt['latest_receipt_info'])
        receipt_list.extend(receipt['receipt']['in_app'])
        latest_time = None
        bundle_id = receipt['receipt']['bundle_id']
        for item in receipt_list:
            product = AppProduct.objects.filter(
                product_id=item['product_id']).first()
            if not product:
                continue
            order_info = instance.get_order_info(
                product, user_id, item, bundle_id)
            if not latest_time or latest_time < order_info['pay_time']:
                latest_time = order_info['pay_time']
            order_list[order_info['order_no']] = {
                "user_id": user_id,
                "payment_id": instance.id,
                "payment_type": payment_type,
            }
            order_list[order_info['order_no']].update(order_info)
            order_list[order_info['order_no']]['extra_info']['receipt'] = item

        instance.b64_receipt = receipt['latest_receipt']
        instance.detail = receipt
        if latest_time:
            instance.last_update_time = latest_time
        instance.save()
        return instance, order_list, renew_status

    @classmethod
    def get_apple_order_no(cls, bid, product_id, purchase_date_ms,
                           user_id):
        purchase_date_ts = int(purchase_date_ms) // 1000
        return "apple-{}-{}-{}-{}".format(
            bid, product_id, purchase_date_ts, user_id)

    def get_order_info(self, product, user_id, receipt: dict, bundle_id) -> \
            (str, dict, float, str):
        """
        Get receipt's order info
        """
        if self.category == 'apple_store':
            purchase_date_ts = int(receipt['purchase_date_ms']) // 1000
            pay_time = timezone.datetime.fromtimestamp(
                purchase_date_ts, tz=timezone.utc)
            expires_date_ts = int(receipt['expires_date_ms']) // 1000
            expires_date = timezone.datetime.fromtimestamp(
                expires_date_ts, tz=timezone.utc)
            expires_date = timezone.localtime(expires_date).date()
            order_no = self.get_apple_order_no(
                bundle_id, receipt['product_id'],
                receipt['purchase_date_ms'], user_id)
            quantity = int(receipt['quantity'])
            related_id = receipt['original_transaction_id']
            is_trial = bool(receipt['is_trial_period'])
            amount = 0 if is_trial else product.price * quantity
            if bool(receipt['is_in_intro_offer_period']) and product.discount:
                amount = amount * product.discount / 10
        else:
            raise TypeError
        return {
            'product': product,
            'order_no': order_no,
            'quantity': quantity,
            'related_id': related_id,
            'amount': amount,
            'pay_time': pay_time,
            'currency': product.currency,
            'extra_info': {
                'type': 'subscription',
                'price': str(product.price),
                'discount': product.discount,
                'expires_date': expires_date.strftime("%Y-%m-%d"),
                'is_trial': is_trial,
            }
        }

    class Meta:
        verbose_name = "AppReceipt"
        verbose_name_plural = verbose_name
        unique_together = (('user_id', 'category'),)


class AppOrder(models.Model):

    product = models.ForeignKey(
        AppProduct, verbose_name="Product", on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(
        verbose_name="Quantity", default=1)
    order_no = models.CharField(
        verbose_name='App Order Unique Id', unique=True, max_length=250)
    user_id = models.IntegerField(
        verbose_name="User Id", db_index=True)
    created = models.DateTimeField(
        verbose_name='Created', default=timezone.now, editable=False)
    pay_time = models.DateTimeField(
        verbose_name="Pay Time")
    amount = models.DecimalField(
        verbose_name="Amount",
        max_digits=8, decimal_places=2,
        default=0,
    )
    currency = models.CharField(
        verbose_name='Currency', max_length=10, default='')
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
    related_id = models.CharField(
        verbose_name="Related Id(Original transaction id)", null=True,
        default=None, max_length=100)

    class Meta:
        verbose_name = "AppOrder"
        verbose_name_plural = verbose_name
