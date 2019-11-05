from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import FilterSet, DjangoFilterBackend
from django_filters import filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework import serializers

from common.common import patch_response
from hupu.view_serializer import *
from hupu.models import *
import logging
from django_bulk_update.helper import bulk_update


# Create your views here.
logger = logging.getLogger(__name__)


class HupuFilterSerializer(FilterSet):
    # 查询需要参数（条件）
    _date = filters.DateFromToRangeFilter(field_name='create_dt')
    _channel_names = filters.BaseInFilter(field_name='channel_names')
    _team = filters.BaseInFilter(field_name='team')
    _account_type = filters.BaseInFilter(field_name='account_type')
    _status = filters.BaseInFilter(field_name='status')
    _used = filters.BaseInFilter(field_name='is_usable')
    _deleted = filters.BaseInFilter(field_name='deleted')
    _jieba_title = filters.CharFilter(field_name='jieba_title', look_expr='icontains')
    
    class Meta:
        # 查询表
        model = Source
        fields = ['_date', '_channel_names', '_team', '_account_type', '_jieba_title', '_status', '_used', '_deleted']
        
        
class SourceNewViewSet(GenericAPIView, mixins.CreateModelMixin):
    serializer_class = SourceSerializer

    def post(self, request, *args, **kwargs):
        '''
        发帖
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        Source.objects.create(**validated_data)
        return patch_response(Response(validated_data))
    

class SourceGetViewSet(GenericAPIView, mixins.RetrieveModelMixin):
    serializer_class = SourceSerializer
    queryset = Source.objects.all()
    
    def get(self, request, *args, **kwargs):
        '''
        获取帖子详情(by id)
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        return self.retrieve(request, *args, **kwargs)
    
    
class SourceListViewSet(GenericAPIView, mixins.ListModelMixin):
    serializer_class = SourceSerializer
    queryset = Source.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_class = HupuFilterSerializer
    lookup_fields = ['date', 'channel_names', 'team', 'account_type', 'jieba_title', 'status', 'used', 'deleted']
    
    def _build_data(self, queryset):
        serializer = self.get_serializer(queryset, many=True)
        house_data = serializer.data
        return house_data
    
    def get(self, request, *args, **kwargs):
        '''
        帖子列表(参数：'page', '_date', '_channel_names', '_team', '_account_type', '_jieba_title', '_status', '_used', '_deleted')
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


class ListSourceSerializer(serializers.Serializer):
    updates = SourceSerializer(many=True)


# class SourceBulkUpdateViewSet(GenericAPIView):
#     serializer_class = ListSourceSerializer
#
#     def post(self, request, *args, **kwargs):
#         '''
#         批量更新
#         :param request: {"updates": [{}, {}]}
#         :param args:
#         :param kwargs:
#         :return:
#         '''
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         validated_data = serializer.validated_data
#         updates = validated_data.updates
#         ids = [i['id'] for i in updates]
#         sources = Source.objects.filter(id__in=ids)
#         datas = {i['id']: i for i in updates}
#         for source in sources:
#             data = datas[source.id]
#             source.mod_title = data['mod_title']
#             source.pred_topic = data['pred_topic']
#             source.status = data['status']
#             source.deleted = data['deleted']
#             source.is_usable = data['is_usable']
#         bulk_update(sources, update_fields=['mod_title', 'pred_topic', 'status', 'deleted', 'is_usable'])
#         return patch_response(Response(updates))
        

class SourceSingleUpdateViewSet(GenericAPIView, mixins.UpdateModelMixin):
    serializer_class = SourceSerializer
    queryset = Source.objects.all()
    
    def post(self, request, *args, **kwargs):
        '''
        更新帖子(by id, 单条更新)
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        return self.update(request, *args, **kwargs)


@api_view(['POST', ])
@csrf_exempt
def bulkUpdate(request):
    '''
    批量更新
    :param request: {"data": [{}, {}]}
    :return:
    '''
    params = request.data.get('data')
    tids = [i['tid'] for i in params]
    print("tids: ", tids)
    sources = Source.objects.filter(tid__in=tids)
    print(params)
    datas = {i['tid']: i for i in params}
    for source in sources:
        data = datas[source.tid]
        source.mod_title = data['mod_title']
        source.pred_topic = data['pred_topic']
        source.status = data['status']
        source.deleted = data['deleted']
        source.is_usable = data['is_usable']
    bulk_update(sources, update_fields=['mod_title', 'pred_topic', 'status', 'deleted', 'is_usable'])
    return patch_response(Response(params))
