from rest_framework import serializers

from .models import Games


class GamesSerialier(serializers.ModelSerializer):
    class Meta:
        model = Games
        fields = "__all__"
