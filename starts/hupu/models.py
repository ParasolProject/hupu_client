from django.db import models
from django_bulk_update.manager import BulkUpdateManager

# Create your models here.


class Source(models.Model):
    id = models.AutoField(primary_key=True, unique=True, editable=False, verbose_name='自增id', db_column='id')
    tid = models.CharField(max_length=30, unique=True, null=True, verbose_name='帖子id', default='', db_column='tid')
    pid = models.CharField(max_length=50, null=True, verbose_name='外站帖子id', default='', db_column='pid')
    title = models.CharField(max_length=255, null=True, verbose_name='帖子标题', default='', db_column='title')
    mod_title = models.CharField(max_length=255, null=True, verbose_name='帖子副标题', default='', db_column='mod_title')
    type = models.IntegerField(null=True, verbose_name='帖子类型', db_column='type')
    topic_id = models.IntegerField(null=True, verbose_name='帖子话题ID', default=0, db_column='topic_id')
    channel_names = models.CharField(max_length=300, verbose_name="分类cate集合 科技 体育 影视 数码",
                                     default='', db_column='channel_names')
    team = models.IntegerField(null=True, verbose_name='团队 1: 篮球 2: 足球 3: 步行街 4: 游戏', default=3, db_column='team')
    account = models.CharField(max_length=100, null=True, verbose_name='帖子采集账号', default='', db_column='account')
    account_name = models.CharField(max_length=100, null=True, verbose_name='帖子采集账号名', default='', db_column='account_name')
    account_type = models.IntegerField(null=True,
                                       verbose_name='账号类别 1:微博2,:即刻,3:抖音,4:B站,5:公众号,6:新浪,7:搜狐,8:皮皮虾,9:,'
                                                    '10:ins,11:西瓜,12:头条,13:it之家,14:鲜知,15:YouTube',
                                       db_column='account_type')
    scheme = models.CharField(max_length=200, null=True, verbose_name='外站URL', default='', db_column='scheme')
    status = models.IntegerField(null=True, verbose_name='帖子使用状态 0: 未使用 2: 已使用', default=0, db_column='status')
    deleted = models.IntegerField(null=True, verbose_name='帖子删除状态', default=0, db_column='deleted')
    is_usable = models.IntegerField(null=True, verbose_name='是否可用', default=0, db_column='is_usable')
    jieba_title = models.CharField(max_length=200, null=True, verbose_name='帖子标题分词', default='', db_column='jieba_title')
    pred_topic = models.CharField(max_length=30, null=True, verbose_name='帖子话题名', db_column='pred_topic')
    pred_prob = models.CharField(max_length=30, null=True, verbose_name='帖子预测话题')
    create_dt = models.DateTimeField(auto_now=True, verbose_name="入库时间", db_column='create_dt')
    update_dt = models.DateTimeField(auto_now=True, verbose_name='更新时间', db_column='update_dt')
    objects = BulkUpdateManager()

    class Meta:
        db_table = 'hupu_posts'
        verbose_name = '帖子全量表'
        verbose_name_plural = verbose_name
        ordering = ['-create_dt']
