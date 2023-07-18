import http.client
import re

from django.shortcuts import render, redirect
from django.http import JsonResponse
# Create your views here.
from django.urls import reverse
from django.views import View
from apps.users.models import User
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
import logging

logger = logging.getLogger('django')
"""
断点的优势:
    1.可以查看我们的方法是否被调用了
    2.可以查看程序在运行过程中的数据
    3.查看程序的执行顺序是否和预期的一致

断点如何添加:
    0.不要在属性,类上加断点
    1.在函数(方法)的入口处
    2.在需要验证的地方添加
"""


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

    def get(self, request):

        return render(request, 'register.html')

    def post(self, request):
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
        if not all([username, password, password2, mobile]):
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
            # 2.6 验证是否同意协议是否勾选
        # 3.入库-----验证数据没问题才入库
        # User.objects.create 直接入库，理论是没问题的，但是，密码是明文
        try:
            user = User.objects.create_user(username=username, password=password, mobile=mobile)
        except Exception as e:
            logger.error(e)
            return render(request, 'register.html', context={'error_message': '数据库异常'})
            return http.HttpResponseBadRequest('数据库异常')
        # 4.返回响应，跳转到首页
        # 注册完成之后,默认认为用户已经登陆了
        # 保持登陆的状态
        # session
        # 自己实现request.session

        # 系统也能自己去帮助我们实现 登陆状态的保持
        from django.contrib.auth import login
        login(request, user)
        # return HttpResponse('注册成功')
        return redirect(reverse('contents:index'))
"""
一 把需求写下来 (前端需要收集什么 后端需要做什么)

二 把大体思路写下来(后端的大体思路)

三 把详细思路完善一下(纯后端)

四 确定我们请求方式和路由


一 把需求写下来 (前端需要收集什么 后端需要做什么)
    当用户把用户名写完成之后,前端应该收集用户名信息, 传递给后端
    后端需要验证 用户名是否重复
二 把大体思路写下来(后端的大体思路)
        前端: 失去焦点之后,发送一个ajax 请求 这个请求包含 用户名
        后端:  接收数据 , 查询用户名
三 把详细思路完善一下
        1. 接收用户名
        2. 查询数据库,通过查询记录的count来判断是否重复 0表示没有重复 1表示重复
四 确定我们请求方式和路由
        敏感数据 推荐使用POST

        GET     usernames/?username=xxxx

        GET     usernames/xxxx/count/  v
"""
# class UsernameCountView(View):
#     def get(self,request,username):
#
#         # 1. 接收用户名
#
#         # 2. 查询数据库,通过查询记录的count来判断是否重复 0表示没有重复 1表示重复
#         try:
#             count = User.objects.filter(username=username).count()
#         except Exception as e:
#             logger.error(e)
#             return JsonResponse({'code': 400, 'errmsg': '数据库异常'})
#         # 3.返回相应
#         return JsonResponse({'code': 0, 'count': count})


class UsernameCountView(View):
    def get(self, request, username):
        # 验证用户名是否满足正则表达式要求
        if re.match(r'^[a-zA-Z0-9_]{5,20}$', username):
            # 处理满足要求的用户名
            try:
                count = User.objects.filter(username=username).count()
            except Exception as e:
                logger.error(e)
                return JsonResponse({'code': 400, 'errmsg': '数据库异常'})
            # 3.返回相应
            return JsonResponse({'code': 0, 'count': count})
            # return JsonResponse({"message": "Valid username"})

        else:
            # 处理不满足要求的用户名
            return JsonResponse({'code': 400, 'errmsg': '用户名规则异常'})
