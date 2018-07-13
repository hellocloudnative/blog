#zhangpengxuan
from django.urls import path,include
from . import views

urlpatterns = [
    path('qq_login',views.qq_login, name='qq_login'),  #qq授权页面
    path('qq_check',views.qq_check,name='qq_check'),   #qq回调页面

]