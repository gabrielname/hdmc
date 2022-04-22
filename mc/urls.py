"""mc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tournament.views import index,table,schedule,participant,account,test

urlpatterns = [
    path('admin/', admin.site.urls),

    #首页
    path('index/',index.index),

    #登录
    path('login/',account.login),
    path('admin_login/',account.admin_login),
    #退出登录
    path('logout/',account.logout),
    #获取验证码图片
    path('image/code/',account.code),

    #积分榜
    path('table/',table.table),
    path('participant_detail/',table.participant_detail),
    #选手详情页数据
    path('pdetail_data/',table.pdetail_data),
    #个人中心
    path('participant_information/',participant.participant_information),

    #选手
    path('participant_add/',participant.participant_add),
    path('participant_delete/',participant.participant_delete),

    #赛程
    path('schedule/',schedule.schedule),
    path('game_add/',schedule.game_add),

    #测试
    path('test/',test.doit),

    
]
