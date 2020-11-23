from django.db import models
from django.utils import timezone


class AppOrder(models.Model):

    user_id = models.IntegerField(
        verbose_name="User Id", db_index=True)
    object_id = models.IntegerField(
        verbose_name="Ojbect Id", null=True, blank=True)
    detail = models.JSONField(
        verbose_name="Detail")
    created = models.DateTimeField(
        verbose_name='Created', default=timezone.now, editable=False)
    category = models.CharField(
        verbose_name="Platform", max_length=32,
        choices=[
            ('apple_store', 'Apple Store',),
        ]
    )

    class Meta:
        verbose_name = "AppOrder"
        verbose_name_plural = verbose_name
