from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_developer = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)

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
    purchase_number = models.PositiveIntegerField(default=0, blank=True)
    developer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now, blank=True)
    ACTION = 'AC'
    ADVENTURE = 'AD'
    COMBAT = 'CO'
    EDUCATIONAL = 'EDU'
    PUZZLE = 'PZ'
    RPG = 'RPG'
    SPORTS = 'SPR'
    STRATEGY = 'STR'
    GAME_CATEGORIES = (
        (ACTION, 'Action'),
        (ADVENTURE, 'Adventure'),
        (COMBAT, 'Combat'),
        (EDUCATIONAL, 'Educational'),
        (PUZZLE, 'Puzzle'),
        (RPG, 'RPG'),
        (SPORTS, 'Sports'),
        (STRATEGY, 'Strategy'),
    )
    category = models.CharField(max_length=20, choices=GAME_CATEGORIES)
    price = models.IntegerField(default=0, blank=True)
    thumbnail = models.ImageField(default='def.jpg', upload_to ='thumbnail', blank = True)


class TransactionManager(models.Manager):
    def create(self, payer, payee, game,amount):
        transaction = self.create(payer=payer, payee= payee, game=game,amount=amount)
        # do something with the transaction
        return transaction

class Transaction(models.Model):
    date = models.DateTimeField(default=timezone.now)
    amount = models.PositiveIntegerField()
    payer = models.ForeignKey(Profile, related_name="Payer", on_delete=models.CASCADE)
    payee = models.ForeignKey(Profile, related_name="Payee", on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    PENDING = 'PE'
    CONFIRMED = 'CO'
    TRANSACTION_CHOICES = (
        (PENDING, 'pending'),
        (CONFIRMED, 'confirmed'),
    )
    state =  models.CharField(max_length=9,choices=TRANSACTION_CHOICES, default=PENDING)
    reference = models.IntegerField(blank=True, null=True)


class Score(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Profile, on_delete=models.CASCADE)
    current_score = models.FloatField(blank=True, null=True)
    #date = models.DateTimeField(default=timezone.now, blank=True)

class State(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Profile, on_delete=models.CASCADE)
    current_state = models.TextField()

    class Meta:
        unique_together = ('game', 'player')