from django.shortcuts import render

# Create your views here.
from backend.models import Profile, Game, Transaction, Score
from rest_framework import viewsets
from playme.restapi.serializers import GameSerializer, TransactionSerializer, ScoreSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  




class GameViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    serializer_class = GameSerializer

    def get_queryset(self):
        return Game.objects.all()



class TransactionViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        user = self.request.user.profile
        prefetch = Transaction.objects.filter(payee = user)
        return prefetch

class ScoreViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = ScoreSerializer

    def get_queryset(self):
        high_scores = Score.objects.order_by('game','-current_score').distinct('game')
        return high_scores


