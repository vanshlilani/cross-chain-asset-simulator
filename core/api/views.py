from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .services import get_crypto_price
from .serializers import AlertSerializer, RegisterSerializer, DepositSerializer, TransactionSerializer, WalletSerializer, TransferSerializer
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .models import Alert, Wallet, Transaction
from decimal import Decimal

import logging

logger = logging.getLogger('api')

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            logger.info(f"User registered: username={serializer.validated_data.get('username')}")
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

        logger.error(f"User registration failed: errors={serializer.errors}")

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "username": request.user.username,
            "role": request.user.role
        })
    

class DepositView(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DepositSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            asset = serializer.validated_data['asset']
            amount = serializer.validated_data['amount']

            with transaction.atomic():
                wallet, created = Wallet.objects.get_or_create(
                    user=user,
                    asset=asset
                )

                wallet.balance += amount
                wallet.save()

                Transaction.objects.create(
                    user=user,
                    asset=asset,
                    type='deposit',
                    amount=amount,
                    status='completed'
                )
            logger.info(f"Deposit success: user={user.username}, asset={asset.symbol}, amount={amount}")
            return Response({
                "message": "Deposit successful",
                "new_balance": wallet.balance
            }, status=status.HTTP_200_OK)

        logger.error(f"Deposit failed: errors={serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PortfolioView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallets = Wallet.objects.filter(user=request.user)
        serializer = WalletSerializer(wallets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TransferView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TransferSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            asset = serializer.validated_data['asset']
            amount = serializer.validated_data['amount']
            from_chain = serializer.validated_data['from_chain']
            to_chain = serializer.validated_data['to_chain']

            try:
                wallet = Wallet.objects.get(user=user, asset=asset)
            except Wallet.DoesNotExist:
                logger.error(f"Transfer failed: user={user.username}, asset={asset.symbol} - Wallet not found")
                return Response({"error": "No balance found"}, status=status.HTTP_400_BAD_REQUEST)

            if wallet.balance < amount:
                logger.error(f"Transfer failed: user={user.username}, asset={asset.symbol}, amount={amount} - Insufficient balance")
                return Response({"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                wallet.balance -= amount
                wallet.save()

                Transaction.objects.create(
                    user=user,
                    asset=asset,
                    type='transfer',
                    amount=amount,
                    from_chain=from_chain,
                    to_chain=to_chain,
                    status='completed'
                )
            logger.info(f"Transfer success: user={user.username}, asset={asset.symbol}, amount={amount}, from={from_chain}, to={to_chain}")
            return Response({
                "message": "Transfer successful",
                "remaining_balance": wallet.balance
            }, status=status.HTTP_200_OK)

        logger.error(f"Transfer validation failed: errors={serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PriceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        symbol = request.query_params.get('asset')

        if not symbol:
            return Response({"error": "Asset is required"}, status=status.HTTP_400_BAD_REQUEST)

        price, error = get_crypto_price(symbol.upper())

        if error:
            logger.error(f"Price fetch failed: asset={symbol}, error={error}")
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)

        logger.info(f"Price fetched: asset={symbol.upper()}, price={price}")
        return Response({
            "asset": symbol.upper(),
            "price_usd": price
        })

class CreateAlertView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AlertSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()

            logger.info(
                f"Alert created: user={request.user.username}, "
                f"asset={request.data.get('asset_symbol')}, "
                f"target={request.data.get('target_price')}"
            )

            return Response(
                {"message": "Alert created"},
                status=status.HTTP_201_CREATED
            )

        logger.error(
            f"Alert creation failed: user={request.user.username}, "
            f"errors={serializer.errors}"
        )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckAlertsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logger.info(f"Checking alerts for user={request.user.username}")

        alerts = Alert.objects.filter(user=request.user, triggered=False)
        triggered_alerts = []

        for alert in alerts:
            price, error = get_crypto_price(alert.asset.symbol)

            if error:
                logger.error(
                    f"Price fetch failed during alert check: "
                    f"asset={alert.asset.symbol}, error={error}"
                )
                continue

            # safer Decimal conversion
            if Decimal(str(price)) >= alert.target_price:
                alert.triggered = True
                alert.save()

                logger.info(
                    f"Alert triggered: user={request.user.username}, "
                    f"asset={alert.asset.symbol}, "
                    f"target={alert.target_price}, "
                    f"current={price}"
                )

                triggered_alerts.append({
                    "asset": alert.asset.symbol,
                    "target_price": alert.target_price,
                    "current_price": price
                })

        return Response(
            {"triggered_alerts": triggered_alerts},
            status=status.HTTP_200_OK
        )
    

class TransactionPagination(PageNumberPagination):
    page_size = 5


class TransactionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user).order_by('-timestamp')

        # 🔍 filter by type
        txn_type = request.query_params.get('type')
        if txn_type:
            transactions = transactions.filter(type=txn_type)

        paginator = TransactionPagination()
        result_page = paginator.paginate_queryset(transactions, request)

        serializer = TransactionSerializer(result_page, many=True)

        logger.info(f"Transactions fetched: user={request.user.username}, filter={txn_type}")
        return paginator.get_paginated_response(serializer.data)