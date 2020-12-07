# Generated by Django 3.1 on 2020-12-07 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConsumeDayLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Date')),
                ('info', models.JSONField(verbose_name='ids')),
            ],
            options={
                'verbose_name': 'ConsumeDayLog',
                'verbose_name_plural': 'ConsumeDayLog',
            },
        ),
    ]