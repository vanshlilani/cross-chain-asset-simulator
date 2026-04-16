from rest_framework import serializers
from .models import Alert, Transaction, User, Asset, Wallet
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['username', 'password', 'role']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            role=validated_data.get('role', 'user')
        )
        return user
    
class DepositSerializer(serializers.Serializer):
    asset_symbol = serializers.CharField()
    amount = serializers.DecimalField(max_digits=20, decimal_places=8)

    def validate(self, data):
        if data['amount'] <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")

        try:
            asset = Asset.objects.get(symbol=data['asset_symbol'], is_active=True)
        except Asset.DoesNotExist:
            raise serializers.ValidationError("Asset not found")

        data['asset'] = asset
        return data
    
class WalletSerializer(serializers.ModelSerializer):
    asset_symbol = serializers.CharField(source='asset.symbol')
    wrapped_symbol = serializers.CharField(source='asset.wrapped_symbol')

    class Meta:
        model = Wallet
        fields = ['asset_symbol', 'wrapped_symbol', 'balance']

class TransferSerializer(serializers.Serializer):
    asset_symbol = serializers.CharField()
    amount = serializers.DecimalField(max_digits=20, decimal_places=8)
    from_chain = serializers.CharField()
    to_chain = serializers.CharField()

    def validate(self, data):
        if data['amount'] <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")

        if data['from_chain'] == data['to_chain']:
            raise serializers.ValidationError("Source and destination chains must differ")

        try:
            asset = Asset.objects.get(symbol=data['asset_symbol'], is_active=True)
        except Asset.DoesNotExist:
            raise serializers.ValidationError("Asset not found")

        data['asset'] = asset
        return data
    

class AlertSerializer(serializers.ModelSerializer):
    asset_symbol = serializers.CharField(write_only=True)

    class Meta:
        model = Alert
        fields = ['asset_symbol', 'target_price']

    def create(self, validated_data):
        user = self.context['request'].user
        symbol = validated_data.pop('asset_symbol')

        try:
            asset = Asset.objects.get(symbol=symbol)
        except Asset.DoesNotExist:
            raise serializers.ValidationError("Asset not found")

        return Alert.objects.create(
            user=user,
            asset=asset,
            **validated_data
        )
        
class TransactionSerializer(serializers.ModelSerializer):
    asset_symbol = serializers.CharField(source='asset.symbol')

    class Meta:
        model = Transaction
        fields = [
            'id',
            'type',
            'asset_symbol',
            'amount',
            'status',
            'from_chain',
            'to_chain',
            'timestamp'
        ]