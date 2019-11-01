from rest_framework import serializers


class AccountSerializer(serializers.Serializer):
    userId = serializers.PrimaryKeyRelatedField()
    pass


class AccountSlitSerializer(serializers.Serializer):
    accountId = serializers.PrimaryKeyRelatedField()
