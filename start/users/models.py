from django.db import models

# Create your models here.


class Base(models.Model):
    id = models.AutoField(primary_key=True, editable=False, db_column='ID')
    createDate = models.DateTimeField(auto_now_add=True, db_column='CREATE_DATE')
    updateDate = models.DateTimeField(auto_now=True, db_column='UPDATE_DATE')

    class Meta:
        abstract = True


class UserDetailsModel(Base):
    name = models.CharField(db_column='NAME', max_length=36, null=True, verbose_name='联系人')
    email = models.CharField(db_column='EMAIL', max_length=36, null=True, verbose_name='邮箱')
    phone = models.CharField(db_column='PHONE', max_length=36, null=True, verbose_name='手机号码')
    balanceAmount = models.DecimalField(db_column='BALANCE_AMOUNT', max_digits=10, decimal_places=2, null=True,
                                        verbose_name='余额', default=0)
    creatorId = models.CharField(db_column='CREATOR_ID', max_length=36, null=True, verbose_name='用户ID')

    class Meta:
        db_table = 'LaunchUserDetails'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
