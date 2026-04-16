from django.contrib import admin
from .models import User, Asset, Wallet, Transaction, Alert

# Register your models here.

admin.site.register(User)
admin.site.register(Asset)
admin.site.register(Wallet)
admin.site.register(Transaction)
admin.site.register(Alert)