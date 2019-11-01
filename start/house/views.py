from django.shortcuts import render
from django_filters.rest_framework import FilterSet, DjangoFilterBackend
from django_filters import filters
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from common.common import patch_response
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin
from house.view_serializer import *
from house.models import *
import logging

# Create your views here.
logger = logging.getLogger(__name__)


class HouseFilterSerializer(FilterSet):
    _province = filters.CharFilter(field_name='province', lookup_expr='icontains')
    _city = filters.CharFilter(field_name='city', lookup_expr='icontains')
    _area = filters.CharFilter(field_name='area', lookup_expr='icontains')
    _price = filters.RangeFilter(field_name='price', lookup_expr='range')
    
    class Meta:
        model = House
        fields = ['_province', '_city', '_area', '_price']


class HouseViewSet(GenericViewSet, CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin):
    serializer_class = HouseSerializer
    queryset = House.objects.filter(status=0)
    filter_backends = (DjangoFilterBackend,)
    filter_class = HouseFilterSerializer
    lookup_fields = ['province', 'city', 'area', 'address', 'price', 'priceType', 'pledge']

    def _build_data(self, queryset):
        serializer = self.get_serializer(queryset, many=True)
        house_data = serializer.data
        return house_data

    def list(self, request, *args, **kwargs):
        '''
        房源信息列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        try:
            sortColumns = kwargs['sortColumn']
            queryset = self.filter_queryset(self.get_queryset()).order_by(sortColumns)
        except Exception as e:
            queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            data = self._build_data(page)
            return self.get_paginated_response(data)
        else:
            data = dict()
            return patch_response(Response(data))
    
    def create(self, request, *args, **kwargs):
        '''
        创建房源信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        validated_data.update({'creatorId': request.user.id})
        data = validated_data.copy()
        imgs = data.pop('imgs')
        house = House.objects.create(**data)
        houseImgs = list()
        for img in imgs:
            houseImgs.append(HouseImg(houseId=house, creatorId=request.user.id, imageUrl=img['imageUrl']))
        HouseImg.objects.bulk_create(houseImgs)
        return patch_response(Response(validated_data))
    
    def update(self, request, *args, **kwargs):
        '''
        更新房源信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        houseId = request.data.get('id')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        
        house = House.objects.get(id=houseId)
        HouseImg.objects.filter(houseId=house).delete()

        data = validated_data.copy()
        imgs = data.pop('imgs')
        newHouse = self.serializer_class().update(instance=house, validated_data=data)
        houseImgs = list()
        for img in imgs:
            houseImgs.append(HouseImg(houseId=newHouse, creatorId=request.user.id, imageUrl=img['imageUrl']))
        HouseImg.objects.bulk_create(houseImgs)
        return patch_response(Response(validated_data))
