from django.urls import path
from . import views
urlpatterns = [
    # 图形验证码
    # url(r'^image_codes/(?P<uuid>[\w-]+)/$', views.ImageCodeView.as_view()),
    path('image_codes/<str:uuid>/', views.ImageCodeView.as_view()),
]