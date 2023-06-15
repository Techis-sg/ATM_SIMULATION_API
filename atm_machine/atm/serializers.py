from rest_framework import serializers
from .models import Card


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'card_number','pin', 'blocked', 'account']
        

class AuthenticateCard(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['card_number','pin']
        

class TokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()


class ObtainTokenSerializer(serializers.Serializer):
    card_number = serializers.CharField()
    pin = serializers.CharField()
