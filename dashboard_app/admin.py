import logging
from django.contrib import admin
from .models import Account, Location

logger = logging.getLogger('dashboard_app')

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'created_at', 'updated_at')
    search_fields = ('name', 'code')
    ordering = ('name',)

    def save_model(self, request, obj, form, change):
        logger.info(f"Admin: {'Updating' if change else 'Creating'} Location: {obj.name}")
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        logger.info(f"Admin: Deleting Location: {obj.name}")
        super().delete_model(request, obj)

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'location', 'opening_date', 'closing_date', 'balance', 'status')
    list_filter = ('location', 'status', 'opening_date')
    search_fields = ('account_number', 'location__name')
    ordering = ('-opening_date',)
    date_hierarchy = 'opening_date'

    def save_model(self, request, obj, form, change):
        logger.info(f"Admin: {'Updating' if change else 'Creating'} Account: {obj.account_number}")
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        logger.info(f"Admin: Deleting Account: {obj.account_number}")
        super().delete_model(request, obj)
