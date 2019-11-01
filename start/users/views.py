from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework import mixins, permissions
from rest_framework.response import Response
from account.models import Account

from users.view_serializer import *
from users.models import *
from common.common import patch_response
import logging


# Create your views here.

logger = logging.getLogger('django')


class RegisterUserView(GenericAPIView, mixins.CreateModelMixin):
    """用户注册"""
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        param = serializer.validated_data
        pwd = param['password']
        username = param['username']
        telephone = param['telephone']
        email = param['email']
        try:
            # 手机号重复
            UserDetailsModel.objects.get(phone=telephone)
            return patch_response(Response(), code=104)
        except Exception as e:
            print("No problem.%s" % e)
        try:
            password = make_password(pwd, None)
            user = User.objects.get_or_create(password=password, username=username)
            Bid = user[0].id
            UserDetailsModel.objects.get_or_create(phone=telephone, creatorId=Bid, name=username, email=email)
            Account.objects.get_or_create(creatorId=Bid)
        except Exception as e:
            print(e)
            # 用户名已存在
            return patch_response(Response(), code=115)
        data = request.POST.copy()
        data['password'] = password
        user = authenticate(username=username, password=pwd)
        login(request, user)
        return patch_response(Response())


class LoginUserView(GenericAPIView):
    """账号密码登陆"""
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        param = serializer.validated_data
        username = param['username']
        password = param['password']
        user = authenticate(username=username, password=password)
        # user账号密码错误
        if user:
            logger.info(request.COOKIES)
            logger.info(request.user)
            login(request, user)
            logger.info(request.COOKIES)
            logger.info(request.user)
            return patch_response(Response({"登陆成功"}))
        return patch_response(Response(), code=117)


class LoginOutUserView(GenericAPIView):
    """登出"""
    pagination_class = None

    def get(self, request, *args, **kwargs):
        logger.info(request.COOKIES)
        logger.info(request.user)
        logout(request)
        logger.info(request.COOKIES)
        logger.info(request.user)
        return patch_response(Response())
    
    
class DetailsUserView(GenericAPIView, mixins.UpdateModelMixin, mixins.ListModelMixin):
    """用户详情信息"""
    serializer_class = DetailsSerializer
    queryset = UserDetailsModel.objects.all()

    def get(self, request, *args, **kwargs):
        self.queryset = UserDetailsModel.objects.filter(creatorId=request.user.id)
        return self.list(self, request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
