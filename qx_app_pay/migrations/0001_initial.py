# Generated by Django 3.1 on 2020-12-02 10:10

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppReceipt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(db_index=True, verbose_name='User Id')),
                ('b64_receipt', models.TextField(null=True, verbose_name='Base64 Query Receipt')),
                ('detail', models.JSONField(verbose_name='Detail')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Created')),
                ('last_update_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Last Update Time')),
                ('last_subscription_info', models.JSONField(default=dict, verbose_name='Subscription Info')),
                ('category', models.CharField(choices=[('apple_store', 'Apple Store')], max_length=32, verbose_name='Platform')),
            ],
            options={
                'verbose_name': 'AppReceipt',
                'verbose_name_plural': 'AppReceipt',
                'unique_together': {('user_id', 'category')},
            },
        ),
        migrations.CreateModel(
            name='AppProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.CharField(max_length=250, verbose_name='Product Identifier')),
                ('name', models.CharField(max_length=255, verbose_name='Product Name')),
                ('desc', models.CharField(max_length=255, verbose_name='Desc')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Price')),
                ('discount', models.DecimalField(decimal_places=2, default=None, max_digits=3, null=True, verbose_name='Price')),
                ('currency', models.CharField(default='', max_length=10, verbose_name='Currency')),
                ('category', models.CharField(choices=[('apple_store', 'Apple Store')], max_length=32, verbose_name='Platform')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
            ],
            options={
                'verbose_name': 'AppProduct',
                'verbose_name_plural': 'AppProduct',
                'unique_together': {('category', 'product_id')},
            },
        ),
        migrations.CreateModel(
            name='AppOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Quantity')),
                ('order_no', models.CharField(max_length=250, unique=True, verbose_name='App Order Unique Id')),
                ('user_id', models.IntegerField(db_index=True, verbose_name='User Id')),
                ('object_id', models.IntegerField(blank=True, default=None, null=True, verbose_name='Ojbect Id')),
                ('object_type', models.CharField(default='', max_length=50, verbose_name='Object Type')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Created')),
                ('pay_time', models.DateTimeField(verbose_name='Pay Time')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Amount')),
                ('currency', models.CharField(default='', max_length=10, verbose_name='Currency')),
                ('extra_info', models.JSONField(default=dict, verbose_name='Extra Info')),
                ('payment_id', models.IntegerField(verbose_name='Payment id')),
                ('payment_type', models.CharField(choices=[('appreceipt', 'AppReceipt')], max_length=32, verbose_name='Payment Type')),
                ('refund', models.BooleanField(default=False, verbose_name='Is Refund')),
                ('related_id', models.CharField(default=None, max_length=100, null=True, verbose_name='Related Id(Original transaction id)')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='qx_app_pay.appproduct', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'AppOrder',
                'verbose_name_plural': 'AppOrder',
            },
        ),
    ]