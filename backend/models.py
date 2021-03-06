from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.shortcuts import reverse
from PIL import Image
import backend.tokens as tokens

# For more info about the models documentation, please check the README.md file in the repository root.

class Profile(models.Model):
    """
    The Profile model.

    Extends the user built-in model.
    """
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
    description = models.TextField()
    link = models.URLField("game_url")
    purchase_number = models.PositiveIntegerField(default=0, blank=True)
    developer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now, blank=True)
    category = models.CharField(max_length=20, choices=tokens.GAME_CATEGORIES)
    price = models.IntegerField(default=0, blank=True)
    thumbnail = models.ImageField(default='def.jpg', upload_to ='thumbnail', blank = True)

    def get_absolute_url(self):
        return reverse('buy', kwargs={'game_id':self.id})
    
    def save(self):
        """ Resizes the thumbnail image uploaded by the developer to 200*200 pixels."""
        super(Game, self).save()
        image = Image.open(self.thumbnail)
        size = (200, 200)
        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.thumbnail.path)

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