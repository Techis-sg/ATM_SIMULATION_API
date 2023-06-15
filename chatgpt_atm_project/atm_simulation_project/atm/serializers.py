from rest_framework import serializers
from .models import User, Card, Account, Transaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class ChangePinSerializer(serializers.Serializer):
    pin = serializers.CharField(max_length=4, min_length=4)

    def validate_pin(self, value):
        try:
            int(value)
        except ValueError:
            raise serializers.ValidationError('PIN should contain only numeric digits.')
        return value


class TokenSerializer(serializers.Serializer):
    cardnumber = serializers.CharField(max_length=16)
    pin = serializers.CharField(max_length=4)

    def validate(self, attrs):
        print("\n inside validate ")
        card_number = attrs.get('cardnumber')
        pin = attrs.get('pin')

        if len(card_number) != 16:
            raise serializers.ValidationError('Invalid card number.')

        try:
            int(card_number)
        except ValueError:
            raise serializers.ValidationError('Card number should contain only numeric digits.')

        if len(pin) != 4:
            raise serializers.ValidationError('Invalid PIN.')

        try:
            int(pin)
        except ValueError:
            raise serializers.ValidationError('PIN should contain only numeric digits.')

        return attrs
