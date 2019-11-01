from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User
# Create your models here.


def _uuid():
    return str(uuid4())


class Account(models.Model):
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False, db_column='ID')
    status = models.IntegerField(default=0)
    creatorId = models.IntegerField(db_column='CREATOR_ID', blank=True, null=True)
    createDate = models.DateTimeField(db_column='CREATE_DATE', auto_now_add=True, blank=True, null=True)
    updateDate = models.DateTimeField(db_column='UPDATE_DATE', auto_now=True, blank=True, null=True)
    
    class Meta:
        db_table = 'account'
        ordering = ['-createDate']


class AccountSlip(models.Model):
    id = models.CharField(max_length=36, primary_key=True, default=_uuid, editable=False, db_column='ID')
    accountId = models.ForeignKey(Account, related_name='account', db_column='ACCOUNT_ID')
    changeAmount = models.DecimalField(db_column='CHANGE_AMOUNT', max_digits=10, decimal_places=2, blank=True,
                                       null=True)
    balanceType = models.IntegerField(db_column='BALANCE_TYPE', blank=True, null=True)
    balance = models.DecimalField(db_column='BALANCE', max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.IntegerField(db_column='STATUS', blank=True, null=True)
    slipDay = models.DateTimeField(db_column='SLIP_DAY', blank=True, null=True)
    creatorId = models.IntegerField(db_column='CREATOR_ID', blank=True, null=True)
    rechargeId = models.CharField(db_column='RECHARGE_ID', default=None, max_length=36, blank=True, null=True)
    createDate = models.DateTimeField(db_column='CREATE_DATE', auto_now_add=True, blank=True, null=True)
    updateDate = models.DateTimeField(db_column='UPDATE_DATE', auto_now=True, blank=True, null=True)
    
    class Meta:
        db_table = 'account_slip'
        ordering = ['-slipDay']
