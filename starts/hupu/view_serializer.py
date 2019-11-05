from rest_framework.serializers import ModelSerializer

from hupu.models import *
import logging


logger = logging.getLogger(__name__)


class SourceSerializer(ModelSerializer):
    
    # def to_representation(self, instance):
    #     return super(SourceSerializer, self).to_representation(instance)
    
    # def update(self, instance, validated_data):
    #     house = super(SourceSerializer, self).update(instance, validated_data)
    #     return house
    
    class Meta:
        model = Source
        fields = '__all__'

