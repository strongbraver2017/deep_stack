from django.db import models
from django.contrib.auth.models import User


class Gambler(models.Model):
    user = models.ForeignKey(User)
    level = models.IntegerField(default=0)
    account_chips = models.FloatField(default=0)
