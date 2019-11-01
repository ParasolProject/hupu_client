from django.contrib.auth.models import User
from django.db import models

# Create your models here.


def upload_img(instance, filename):
    import os
    from django.utils.timezone import now
    filename_base, filename_ext = os.path.splitext(filename)
    path = 'imageUrl/%s%s' % (now().strftime("%Y%m%d%H%M%S"), filename_ext.lower(),)
    return path


class PriceType(object):
    Month = 1
    Season = 2
    Half = 3
    Year = 4
    CHOICES = (
        (Month, '月付'),
        (Season, '季付'),
        (Half, '半年付'),
        (Year, '年付'),
    )


class Base(models.Model):
    id = models.AutoField(primary_key=True, editable=False, db_column='ID')
    createDate = models.DateTimeField(auto_now_add=True, db_column='CREATE_DATE')
    updateDate = models.DateTimeField(auto_now=True, db_column='UPDATE_DATE')

    class Meta:
        abstract = True


class House(Base):
    status = models.IntegerField(default=0, verbose_name='状态', db_column='STATUS')
    province = models.CharField(max_length=10, null=False, verbose_name='省份', db_column='PROVINCE')
    city = models.CharField(max_length=20, null=False, verbose_name='城市', db_column='CITY')
    area = models.CharField(max_length=50, null=False, verbose_name='区域', db_column='AREA')
    address = models.CharField(max_length=500, verbose_name='详细地址', null=False, db_column='ADDRESS')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, verbose_name='价格', db_column='PRICE')
    priceType = models.IntegerField(null=True, verbose_name='支付方式', choices=PriceType.CHOICES, db_column='PRICE_TYPE')
    pledge = models.DecimalField(max_digits=10, decimal_places=2, null=False, verbose_name='押金', db_column='PLEDGE')
    creatorId = models.CharField(max_length=255, null=True, verbose_name='用户id', blank=True, db_column='CREATOR_ID')
    
    class Meta:
        db_table = 'House'
        verbose_name = '房屋信息'
        verbose_name_plural = verbose_name
        ordering = ['-createDate']


class HouseImg(Base):
    houseId = models.ForeignKey(House, related_name='house', verbose_name='房间ID', db_column='HOUSE_ID')
    status = models.IntegerField(default=0, verbose_name='状态')
    imageUrl = models.FileField(upload_to=upload_img, null=True, blank=True, verbose_name='图片地址', db_column='IMAGE_URL')
    creatorId = models.CharField(max_length=255, null=True, verbose_name='用户id', blank=True, db_column='CREATOR_ID')
    
    class Meta:
        db_table = 'HouseImg'
        verbose_name = '房屋图片'
        verbose_name_plural = verbose_name
        ordering = ['-createDate']
        

class RentInfo(Base):
    pass
