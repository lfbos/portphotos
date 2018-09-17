from django.contrib.auth.models import AbstractUser
from django.db import models

from core.mixins import BaseMixin


class CustomUser(AbstractUser, BaseMixin):
    access_token = models.CharField(max_length=512, blank=True, null=True)
    account_id = models.CharField(max_length=256, blank=True, null=True)
    user_id = models.CharField(max_length=64, blank=True, null=True)

    @property
    def is_dropbox_account_linked(self):
        return self.access_token is not None
