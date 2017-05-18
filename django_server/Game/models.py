from django.db import models
from django.contrib.postgres.fields import JSONField


class GameRecord(models.Model):
    gambler_hands_json = JSONField(max_length=512)
    operations_json = JSONField(max_length=1024)
    game_result_json = JSONField(max_length=1024)
    level_by_bigblind = models.IntegerField()
