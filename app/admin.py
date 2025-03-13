from django.contrib import admin

from app import models

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ("handle",)

class WalletAdmin(admin.ModelAdmin):
    list_display = ("address", "private_key", "user")


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Wallet, WalletAdmin)