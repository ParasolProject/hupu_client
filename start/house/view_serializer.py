from house.models import *
from rest_framework import serializers
import logging


logger = logging.getLogger(__name__)


class HouseImgSerializer(serializers.ModelSerializer):
    imageUrl = serializers.CharField(required=False, allow_null=True)
    
    class Meta:
        model = HouseImg
        fields = ['imageUrl', ]


class HouseSerializer(serializers.ModelSerializer):
    imgs = HouseImgSerializer(many=True, required=False)
    
    def to_representation(self, instance):
        house = super(HouseSerializer, self).to_representation(instance)
        house_data = dict(house)
        imgs = HouseImg.objects.filter(houseId=house_data['id'], status=0).values('imageUrl')
        house_data['imgs'] = imgs
        return house_data
    
    def update(self, instance, validated_data):
        house = super(HouseSerializer, self).update(instance, validated_data)
        return house
    
    class Meta:
        model = House
        fields = '__all__'
