from rest_framework import serializers
from .models import User


class AccountSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ("id", "email", "password",)


class TokenSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ("id", "email",)
