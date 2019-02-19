from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.profile.email_confirmed)
        )

account_activation_token = AccountActivationTokenGenerator()


ACTION = 'Action'
ADVENTURE = 'Adventure'
COMBAT = 'Combat'
EDUCATIONAL = 'Educational'
PUZZLE = 'Puzzle'
RPG = 'RPG'
SPORTS = 'Sports'
STRATEGY = 'Strategy'
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