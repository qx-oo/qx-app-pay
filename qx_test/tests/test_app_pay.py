import pytest
import json
from django.contrib.auth.models import User
from qx_app_pay.viewsets import apple_subscription
from qx_app_pay.models import AppProduct, AppOrder


class TestViewsets:

    @pytest.mark.django_db
    def test_apple_subscription(self, client):
        url = "/apple-pay/subscription/"
        # viewset = apple_subscription

        AppProduct.objects.create(
            product_id='cn..enjoy03ars',
            name="Product 1",
            desc="test", price="9.9",
            category='apple_store')
        AppProduct.objects.create(
            product_id='cn..enjoy03t1ars',
            name="Product 2",
            desc="test", price="19.9",
            category='apple_store')

        username = 'shawn'
        password = 'test1234'
        user = User.objects.create_user(
            username=username, email='shawn@test.com', password=password)
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
