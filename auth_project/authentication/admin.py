from django.contrib import admin
from .models import AuthToken

@admin.register(AuthToken)
class AuthTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at', 'expires_at', 'is_valid')
    search_fields = ('user__username', 'token')
    list_filter = ('is_valid',)