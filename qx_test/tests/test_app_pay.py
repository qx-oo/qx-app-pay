import pytest
from django.utils import timezone
from django.contrib.auth.models import User
from qx_app_pay.models import AppProduct, AppOrder
from qx_test.members.models import UserInfo
from qx_test.members.tasks import MyUpdateVipReceiptTask


class TestViewsets:

    @pytest.mark.django_db
    def test_apple_subscription(self, client):
        url = "/apple-pay/subscription/"
        # viewset = apple_subscription

        AppProduct.objects.create(
            product_id='cn....',
            name="Product 1",
            desc="test", price="9.9",
            category='apple_store')
        AppProduct.objects.create(
            product_id='cn....',
            name="Product 2",
            desc="test", price="19.9",
            category='apple_store')

        username = 'shawn'
        password = 'test1234'
        user = User.objects.create_user(
            username=username, email='shawn@test.com', password=password)
        UserInfo.objects.create(user=user)
        client.login(username=username, password=password)

        data = {
            "b64_receipt": r"""""",
        }
        resp = client.post(
            url, data=data,
            content_type='application/json')
        assert resp.status_code == 200
        num = AppOrder.objects.filter(user_id=user.id).count()
        assert num > 0

        userinfo = UserInfo.objects.get(user_id=user.id)
        _ = userinfo.is_vip()
        assert userinfo.vip_expire_date
        assert len(userinfo.vip_order['used_ids']) > 0

        userinfo.vip_expire_date = timezone.localtime(timezone.now()).date()
        userinfo.save()
        MyUpdateVipReceiptTask().run(_type=1)
        print('test')
