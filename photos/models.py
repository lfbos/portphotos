from django.contrib.auth.models import AbstractUser
from django.db import models

from core.mixins import BaseMixin


class CustomUser(AbstractUser, BaseMixin):
    dropbox_api_key = models.CharField(max_length=512, blank=True, null=True)

    @property
    def is_dropbox_account_linked(self):
        return self.dropbox_api_key is not None
