from django.contrib.auth.models import User
from django.shortcuts import render, redirect


from mysite import  settings
from django.http import  HttpResponseRedirect
from oauth.oauth_client import oAuth_QQ
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import  logout as auth_logout

import time
from .models import OAuth_ex
# Create your views here.
def qq_login(request):
    #进入到QQ登录界面
    oauth_QQ=oAuth_QQ(settings.QQ_APP_ID,settings.QQ_KEY,settings.QQ_RECALL_URL)
    url=oauth_QQ.get_auth_url()
    return HttpResponseRedirect(url)


def qq_check(request):
  return