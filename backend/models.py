from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_developer = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

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
    developer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.now, blank=True)
    #category ??

class Transaction(models.Model):
    date = models.DateTimeField(default=datetime.now)
    amount = models.PositiveIntegerField()
    payer = models.ForeignKey(Profile, related_name="Payer", on_delete=models.CASCADE)
    payee = models.ForeignKey(Profile, related_name="Payee", on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    #state ??

class Score(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Profile, on_delete=models.CASCADE)
    current_score = models.PositiveIntegerField(default=0)
    date = models.DateField(default=datetime.now, blank=True)