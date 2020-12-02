from django.db import models
from django.conf import settings

# Create your models here.


class Members(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Members'
        verbose_name_plural = verbose_name
