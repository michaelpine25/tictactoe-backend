from django.db import models

class Game(models.Model):
    player_1_id = models.IntegerField()
    player_2_id = models.IntegerField(null=True)
    player_1_moves = models.CharField(max_length=255, default='')
    player_2_moves = models.CharField(max_length=255, default='')
    code = models.IntegerField(unique=True, null=True)
    turn = models.IntegerField(default=1)
    active = models.BooleanField(default=True)
    winner_id = models.IntegerField(null=True)
