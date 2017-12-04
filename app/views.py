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

def redirect_url(request):
    title = request.GET.get('title')
    code = request.GET.get('code')
    state = request.GET.get('state')
    next_url = request.GET.get('next')
    redirect_url = request.GET.get('redirect_url')
    if code == '100':
        title = '成功！'
        state = '登录成功，即将跳转。'
        redirect_url = next_url or '/user/'
    elif code == '101':
        title = '成功！'
        state = '注册成功，即将跳转。'
        redirect_url = next_url or '/auth/login'
    elif code == '102':
        title = '成功！'
        state = '登出成功，即将跳转。'
        redirect_url = next_url or '/auth/login'
    else:
        pass
    return render(request, 'redirect.html', locals())



def user_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/user/')

    next_url = request.GET.get('next')
    state = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember')
        next_url = request.POST.get('next_url')

        user = auth.authenticate(username=username, password=password)

        if user:
            if remember_me:
                request.session.set_expiry(60*60*24*14)
            if user.is_active:
                auth.login(request, user)
                if next_url:
                    return HttpResponseRedirect('/redirect/?code=100&next=%s'%next_url)
                return HttpResponseRedirect('/redirect/?code=100')
            else:
                state = 'not_active'
        else:
            state = 'not_exist_or_password_error'


    return render(request, 'auth/login.html', locals())


def about(request):
    return HttpResponse("这是关于页面")


@login_required
def user_logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/redirect/?code=102')

def user_register(request):
    username = '用户名'
    email = '邮箱'
    password = '密码'
    repeat_password = '重复密码'

    if request.user.is_authenticated():
        return HttpResponseRedirect('/user/')
    state = None
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        if password == '' or repeat_password == '' or password == '密码' or repeat_password == '重复密码' or username == '' or username == '用户名' or email == '' or email == '邮箱':
            username = username or '用户名'
            email = email or '邮箱'
            password = password or '密码'
            repeat_password = repeat_password or '重复密码'
            state = 'empty'
        elif password != repeat_password:
            state = 'repeat_error'
        else:
            if Uzser.objects.filter(username=username):
                state = 'user_exist'
            elif User.objects.filter(email=email):
                state = 'email_exist'
            else:
                new_user = User.objects.create(username=username)
                new_user.save()
                state = 'success'
                auth.login(request, new_user)
    return render(request, 'auth/register.html', locals())

def password_reset(request):
    return HttpResponse("这是密码重置页面")


@login_required
def user_index(request):
    active_nav = 'dashboard'
    user = request.user
    title = "IAAP | 控制面板"
    return render(request, 'user/index.html', locals())


@login_required
def profile(request):
    user = request.user
    title = "IAAP | 用户资料"
    state = None
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        repeat_password = request.POST.get('repeat_password')

        if user.check_password(old_password):
            if not new_password:
                state = 'empty'
            elif new_password != repeat_password:
                state = 'repeat_error'
            else:
                user.set_password(new_password)
                user.save()
                state = 'success'

    return render(request, 'user/profile.html', locals())


@login_required
def code(request):
    return HttpResponse("这是兑换码页")


@login_required
def print_index(request):
    return HttpResponse("这是打印首页")


@login_required
def announcement(request):
    return HttpResponse("这是公告页")

def page_error(request):
    return render(request, 'error.html')
