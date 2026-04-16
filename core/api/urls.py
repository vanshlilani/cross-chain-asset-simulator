from django.urls import path
from .views import CheckAlertsView, CreateAlertView, DepositView, MeView, PortfolioView, PriceView, RegisterView, TransactionListView, TransferView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', MeView.as_view(), name='me'),
    path('deposit/', DepositView.as_view(), name='deposit'),
    path('portfolio/', PortfolioView.as_view(), name='portfolio'),
    path('transfer/', TransferView.as_view(), name='transfer'),
    path('price/', PriceView.as_view(), name='price'),
    path('alerts/', CreateAlertView.as_view(), name='create-alert'),
    path('alerts/check/', CheckAlertsView.as_view(), name='check-alerts'),
    path('transactions/', TransactionListView.as_view(), name='transactions'),
]