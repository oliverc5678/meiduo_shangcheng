import re

from django.http import HttpResponse

from apps.verifications.constants import IMAGE_CODE_EXPIRE_TIME
from libs.captcha.captcha import captcha
from django.shortcuts import render
from django_redis import get_redis_connection

# Create your views here.
from django.views import View

"""
一 把需求写下来 (前端需要收集什么 后端需要做什么)
    前端需要生成一个随机码（uuid），把这个随机码给后端
    后端需要生成图片验证码，把这个图片验证码的内容保存到redis中，redis的数据是uuid：xxxx
二 把大体思路写下来(后端的大体思路)
    1、生成图片验证码和获取图片验证码的内容
        2.1、连接redis，
        2.2、将图片验证码保存起来，uuid：xxxx有效期
    3、返回图片验证码
三 把详细思路完善一下(纯后端)
    1、生成图片验证码和获取图片验证码的内容
        2.1、连接redis，
        2.2、将图片验证码保存起来，uuid：xxxx有效期
    3、返回图片验证码
四 确定我们请求方式和路由
    GET     image_codes/(?P<uuid>[\w-]+)/
    GET     image_codes/?uuid=xxxxx
"""


class ImageCodeView(View):

    def get(self, request, uuid):
        if re.match(r'^[\w-]+$', uuid):
            # 1、生成图片验证码和获取图片验证码的内容
            text, image = captcha.generate_captcha()
            # 2.1、连接redis，
            redis_conn = get_redis_connection('code')
            # 2.2、将图片验证码保存起来，uuid：xxxx有效期
            # redis_conn.setex(key,seconds,value)
            # redis_conn.setex(uuid,120,text)
            # 加一个前缀
            # redis_conn.setex('img_%s' % uuid, 120, text)
            # 增加了代码的可读性
            redis_conn.setex('img_%s' % uuid, IMAGE_CODE_EXPIRE_TIME, text)
            # 3、返回图片验证码
            # 告知浏览器这是一个图片
            return HttpResponse(image, content_type='image/jpeg')
        else:
            pass
