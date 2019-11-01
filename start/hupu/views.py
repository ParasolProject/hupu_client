from django.db.models import Q
from django.shortcuts import render
from django_filters.rest_framework import FilterSet, DjangoFilterBackend
from django_filters import filters
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from common.common import patch_response
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin
from hupu.view_serializer import *
from hupu.models import *
import logging
from django.views.decorators.csrf import csrf_exempt
from django_bulk_update.helper import bulk_update


# Create your views here.
logger = logging.getLogger(__name__)


class HupuFilterSerializer(FilterSet):
    _status = filters.BaseInFilter(field_name='status')
    _used = filters.BaseInFilter(field_name='is_usable')
    _deleted = filters.BaseInFilter(field_name='deleted')
    _date = filters.DateFromToRangeFilter(field_name='createDate')
    _plate = filters.BaseInFilter(field_name='plate')
    _topic = filters.BaseInFilter(field_name='topic')
    
    class Meta:
        model = Source
        fields = ['_status', '_used', '_deleted', '_date', '_plate', '_topic']
        

class SourceListViewSet(GenericViewSet, CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin):
    serializer_class = SourceSerializer
    queryset = Source.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_class = HupuFilterSerializer
    lookup_fields = ['status', 'is_usable', 'deleted', 'createDate', 'plate', 'topic']
    
    def _build_data(self, queryset):
        serializer = self.get_serializer(queryset, many=True)
        house_data = serializer.data
        return house_data
    
    def create(self, request, *args, **kwargs):
        '''
        发帖
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        logging.info(self.request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        Source.objects.create(**validated_data)
        return patch_response(Response(validated_data))
    
    def list(self, request, *args, **kwargs):
        '''
        帖子列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            data = self._build_data(page)
            return self.get_paginated_response(data)
        else:
            data = dict()
            return patch_response(Response(data))

    def update(self, request, *args, **kwargs):
        '''
        更新帖子
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        sourceId = request.data.get('id')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
    
        house = Source.objects.get(id=sourceId)
    
        self.serializer_class().update(instance=house, validated_data=validated_data)
        return patch_response(Response(validated_data))


@api_view(['POST', ])
@csrf_exempt
def bulkUpdate(request):
    '''
    批量更新
    :param request: {"data": [{}, {}]}
    :return:
    '''
    params = request.data.get('data')
    ids = [i['id'] for i in params]
    sources = Source.objects.filter(id__in=ids)
    datas = {i['id']: i for i in params}
    for source in sources:
        data = datas[source.id]
        source.subhead = data['subhead']
        source.topic = data['topic']
        source.status = data['status']
        source.deleted = data['deleted']
        source.is_usable = data['is_usable']
    bulk_update(sources, update_fields=['subhead', 'topic', 'status', 'deleted', 'is_usable'])
    return patch_response(Response(params))
