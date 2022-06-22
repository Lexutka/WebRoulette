from django.db import models
from django.conf import settings


class Round(models.Model):   # Сохраняем состояние раунда в данный момент времени
    one = models.IntegerField('1', default=1, null=True)
    two = models.IntegerField('2', default=2, null=True)
    three = models.IntegerField('3', default=3, null=True)
    four = models.IntegerField('4', default=4, null=True)
    five = models.IntegerField('5', default=5, null=True)
    six = models.IntegerField('6', default=6, null=True)
    seven = models.IntegerField('7', default=7, null=True)
    eight = models.IntegerField('8', default=8, null=True)
    nine = models.IntegerField('9', default=9, null=True)
    ten = models.IntegerField('10', default=10, null=True)
    jackpot = models.CharField('Jackpot', max_length=10, default='Jackpot!', null=True)

    def __str__(self):
        return str(self.id)


class RollLog(models.Model):   # Сохраняем информацию о каждом ходе (игрок, номер раунда, выпавшее число)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    roll_round = models.ForeignKey(Round, on_delete=models.CASCADE)
    roll_num = models.CharField(max_length=25)

    def __str__(self):
        return str(self.roll_num)


class RoundLog(models.Model):   # Сохраняем кол-во участников раунда-n
    round_num = models.ForeignKey(Round, on_delete=models.CASCADE)
    players_amount = models.IntegerField('Участников в раунде', default=0)

    def __str__(self):
        return str(self.round_num)


class ActivityLog(models.Model):   # Сохраняем активность игроков (id, кол-во раундов, кол-во ходов)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rounds_amount = models.IntegerField(default=0, auto_created=True)
    rolls_amount = models.IntegerField(default=0, auto_created=True)