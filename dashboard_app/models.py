import logging
from django.db import models

logger = logging.getLogger('dashboard_app')

# Create your models here.

class Location(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'locations'
        managed = False  # This tells Django not to manage the table

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        logger.info(f"Saving location: {self.name} (ID: {self.id})")
        super().save(*args, **kwargs)

class Account(models.Model):
    id = models.IntegerField(primary_key=True)
    account_number = models.CharField(max_length=20)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, db_column='location_id')
    opening_date = models.DateField()
    closing_date = models.DateField(null=True, blank=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'accounts'
        managed = False  # This tells Django not to manage the table
        indexes = [
            models.Index(fields=['opening_date']),
            models.Index(fields=['closing_date']),
            models.Index(fields=['location']),
        ]


    def __str__(self):
        return f"{self.account_number} - {self.location.name}"

    def save(self, *args, **kwargs):
        logger.info(f"Saving account: {self.account_number} (ID: {self.id})")
        super().save(*args, **kwargs)
