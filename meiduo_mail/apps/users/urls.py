from django.urls import path, re_path

from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    # re_path(r'^usernames/(?P<username>[a-zA-Z0-9_]{5,20})/count/$', views.UsernameCountView.as_view(),name='usernamecount'),
    path('usernames/<str:username>/count/', views.UsernameCountView.as_view(), name='usernamecount'),
]
