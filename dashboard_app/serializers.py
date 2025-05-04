import logging
from rest_framework import serializers
from .models import Account, Location

logger = logging.getLogger('dashboard_app')

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

    def to_representation(self, instance):
        logger.debug(f"Serializing Location: {instance.name}")
        return super().to_representation(instance)

    def to_internal_value(self, data):
        logger.debug(f"Deserializing Location data: {data}")
        return super().to_internal_value(data)

class AccountSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    location_id = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(),
        source='location',
        write_only=True
    )

    class Meta:
        model = Account
        fields = '__all__'

    def to_representation(self, instance):
        logger.debug(f"Serializing Account: {instance.account_number}")
        return super().to_representation(instance)

    def to_internal_value(self, data):
        logger.debug(f"Deserializing Account data: {data}")
        return super().to_internal_value(data) 