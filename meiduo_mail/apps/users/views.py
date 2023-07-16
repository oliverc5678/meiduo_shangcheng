import http.client
import re

from django.shortcuts import render

# Create your views here.
from django.views import View
from apps.users.models import User
from django.http import HttpResponseBadRequest
from django.http import HttpResponse

class RegisterView(View):
    """
    1.用户名我们需要判断是否重复(这个要开发一个视图)
            用户名的长度有5-20个的要求
    2.密码 有长度的限制 8-20 要求为 字母,数字,_
    3.确认密码 和密码一致
    4.手机号   手机号得先满足规则
        再判断手机号是否重复
    5.图片验证码是一个后端功能
        图片验证码是为了防止 计算机攻击我们发送短信的功能
    6.短信发送
    7.必须同意协议
    8.注册也是一个功能


    必须要和后端交互的是:
        1.用户名/手机号是否重复
        2.图片验证码
        3.短信
        4.注册功能
    """
    def get(self,request):

        return render(request,'register.html')


    def post(self,request):
        """
        1.接收前端提交的用户名,密码和手机号
        2.数据的验证（不相信前端提交的任何数据）
            2.1 验证必传的数据（前端传给后端）是否有值
            2.2 判断用户名
            2.3 判断密码
            2.4 确认密码和密码是否一致
            2.5 判断手机号是否符合规则
        2.入库-----必须得有模型（转移思路）
        3.返回相应
        """
        # 1.接收前端提交的用户名,密码和手机号
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        password2 = data.get('password2')
        mobile = data.get('mobile')
        # 2.数据的验证（不相信前端提交的任何数据）
        #     2.1 验证必传的数据（前端传给后端）是否有值
        #     all([el,el,el])el必须有值，只要有一个为None，则为Falese
        if not all([username,password,password2,mobile]):
            return HttpResponseBadRequest('参数有问题')
            # 2.2 判断用户名是否符合规则，判断5-20位数字 字母 _组合
        if not re.match(r'^[a-zA-Z0-9_]{5,20}$', username):
            return HttpResponseBadRequest('用户名不合法')
            # 2.3 判断密码是否符合规则，要求8-20位字 字母 _组合
        if not re.match(r'^[a-zA-Z0-9_]{8,20}$', password):
            return HttpResponseBadRequest('密码不合法')
            # 2.4 判断密码是否一致
        if password != password2:
            return HttpResponseBadRequest('密码不一致')
            # 2.5 判断手机号是否符合规则
        if not re.match(r'^1[3456789]\d{9}$', mobile):
            return HttpResponseBadRequest('手机号不符合规则')
        # 3.入库-----验证数据没问题才入库
        # User.objects.create 直接入库，理论是没问题的，但是，密码是明文
        user = User.objects.create_user(username=username, password=password, mobile=mobile)
        # 4.返回响应
        # return http.HttpResponse('注册成功')
        return HttpResponse('注册成功')
