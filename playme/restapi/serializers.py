from backend.models import Profile, Game, Score, Transaction
from rest_framework import serializers

class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        fields = ('name', 'description', 'category', 'price')


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('date', 'game', 'amount', 'state', 'reference')


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ('game', 'player', 'current_score')
