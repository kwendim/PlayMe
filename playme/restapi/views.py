from django.shortcuts import render

# Create your views here.
from backend.models import User, Game
from rest_framework import viewsets
from playme.restapi.serializers import GameSerializer


class GameViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer