from django.contrib.auth.models import AbstractUser
from django.db import models
from simple_history.models import HistoricalRecords
from simple_history import register
from django.contrib.auth.models import Group, Permission

register(Group)
register(Permission)


class User(AbstractUser):
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    history = HistoricalRecords(m2m_fields=["groups", "user_permissions"])
