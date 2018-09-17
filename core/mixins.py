import uuid

from django.contrib.postgres.fields import JSONField
from django.db import models


class BaseMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    metadata = JSONField(
        blank=True,
        default=dict,
        verbose_name='metadata'
    )
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name='date and time of creation'
    )
    updated = models.DateTimeField(
        auto_now=True,
        editable=False,
        verbose_name='date and time of last update'
    )

    class Meta:
        abstract = True
