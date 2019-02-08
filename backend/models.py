from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

#from django.db.models.signals import post_save
#from django.dispatch import receiver
from datetime import datetime

# Create your models here.

class Developer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Game(models.Model):
    name = models.CharField(max_length=255, unique=True)
    rating = models.PositiveIntegerField(
        default=0,
        blank=True,
        validators=[MaxValueValidator(5),
            MinValueValidator(0)
        ])
    high_score = models.PositiveIntegerField(default=0, blank=True)
    description = models.TextField(blank=True)
    link = models.URLField("game_url")
    number_of_purchases = models.PositiveIntegerField(default=0, blank=True)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.now, blank=True)
    #category ??

class Transaction(models.Model):
    date = models.DateTimeField(default=datetime.now)
    amount = models.PositiveIntegerField()
    payer = models.ForeignKey(User, on_delete=models.CASCADE)
    payee = models.ForeignKey(Developer, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    #state ??

class Score(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    current_score = models.PositiveIntegerField(default=0)
    date = models.DateField(default=datetime.now, blank=True)