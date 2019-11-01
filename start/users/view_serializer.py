from rest_framework import serializers
from users.models import *


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    telephone = serializers.CharField(required=True)
    email = serializers.EmailField(required=False)


class DetailsSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "createDate": instance.createDate,
            "updateDate": instance.updateDate,
            "name": instance.name,
            "email": instance.email,
            "phone": instance.phone.replace(instance.phone[3:7], '****'),
            "balanceAmount": instance.balanceAmount,
            "creatorId": instance.creatorId
        }

    class Meta:
        model = UserDetailsModel
        fields = '__all__'
