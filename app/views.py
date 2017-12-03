#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django import forms
from django.contrib import auth
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import Profile, BalanceLog, Printer, PrinterOptions, PrintJobs, RedeemCode


def index(request):
    return HttpResponse("首页")

def user_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    state = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user:
            if user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse(u'你的账户未启用，请联系管理员。')
        else:
            state = 'not_exist_or_password_error'

    context = {
        # 'loginForm': LoginForm(),
        # 'state': state,
    }

    return render(request, 'auth/login.html', context)


def about(request):
    return HttpResponse("这是关于页面")


def user_logout(request):
    return HttpResponse("这是登出页面")


def user_register(request):
    return HttpResponse("这是注册页面")

def password_reset(request):
    return HttpResponse("这是密码重置页面")

def user_index(request):
    user = request.user
    title = "IAAP | 控制板"
    return render(request, 'user/index.html', locals())

def profile(request):
    return HttpResponse("这是用户信息页")

def code(request):
    return HttpResponse("这是兑换码页")

def print_index(request):
    return HttpResponse("这是打印首页")

def announcement(request):
    return HttpResponse("这是公告页")
