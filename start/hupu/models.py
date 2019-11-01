from django.db import models
from django_bulk_update.manager import BulkUpdateManager

# Create your models here.


class Source(models.Model):
    id = models.AutoField(primary_key=True, editable=False, db_column='ID')
    title = models.CharField(max_length=255, null=True, verbose_name='帖子标题', db_column='TITLE')
    subhead = models.CharField(max_length=255, null=True, verbose_name='帖子副标题', db_column='SUBHEAD')
    transRate = models.FloatField(max_length=20, null=True, verbose_name='离线转化率', db_column='TRANS_RATE')
    topic = models.CharField(max_length=255, null=True, verbose_name='帖子话题', db_column='TOPIC')
    recommend = models.DecimalField(max_digits=3, decimal_places=1, null=True, verbose_name='推荐数', db_column='RECOMMEND')
    recuperate = models.IntegerField(null=True, verbose_name='回帖数', db_column='RECUPERATE')
    lightRecuperate = models.IntegerField(null=True, verbose_name='亮回帖数', db_column='LIGHT_RECUPERATE')
    createDate = models.DateTimeField(auto_now_add=True, verbose_name='发帖时间', db_column='CREATE_DATE')
    plate = models.CharField(max_length=255, null=True, verbose_name='版块', db_column='PLATE')
    status = models.IntegerField(null=True, verbose_name='帖子使用状态', db_column='STATUS')
    deleted = models.IntegerField(null=True, verbose_name='帖子删除状态', db_column='DELETED')
    is_usable = models.IntegerField(null=True, verbose_name='是否可用', db_column='IS_USED')
    updateDate = models.DateTimeField(auto_now=True, verbose_name='更新时间', db_column='UPDATE_DATE')
    objects = BulkUpdateManager()
    
    class Meta:
        db_table = 'Hupu'
        verbose_name = '帖吧'
        verbose_name_plural = verbose_name
        ordering = ['-createDate']
