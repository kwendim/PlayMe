from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """
    A token generator for email activation.

    Mixes the current timestamp with the user primary key (user_id) to generate
    a hash value as a part of the email verification link.
    """
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.profile.email_confirmed)
        )

account_activation_token = AccountActivationTokenGenerator()

# Enum for Game Categories. Used by the Game Model and the Upload Form.
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