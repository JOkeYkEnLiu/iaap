#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django import forms
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.conf import settings

# Create your views here.
from .models import Profile, BalanceLog, Printer, PrinterOptions, PrintJobs, RedeemCode, User
from app.pdf_page_count import getPDFPages
from django.core.files.base import ContentFile
import random
import string

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
                if next_url != 'None':
                    return HttpResponseRedirect('/redirect/?code=100&next=%s'%next_url)
                return HttpResponseRedirect('/redirect/?code=100')
            else:
                state = 'not_active'
        else:
            state = 'not_exist_or_password_error'


    return render(request, 'auth/login.html', locals())


@login_required
def user_logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/redirect/?code=102')


def user_register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/user/')
    state = None
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        if password == '' or repeat_password == '' or username == '' or email == '':
            state = 'empty'
        elif password != repeat_password:
            state = 'repeat_error'
        else:
            if User.objects.filter(username=username):
                state = 'user_exist'
            elif User.objects.filter(email=email):
                state = 'email_exist'
            else:
                new_user = User.objects.create(username=username,email=email,password=password)
                new_user.save()
                state = 'success'
                auth.login(request, new_user)
    return render(request, 'auth/register.html', locals())


def password_reset(request):
    return render(request, 'auth/password_reset.html')


def about(request):
    return HttpResponse("这是关于页面")


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


@login_required
def new_print_job(request):
    title = "IAAP | 开始打印" 
    active_nav = 'printjobs'
    if request.method == 'POST':
        t = datetime.datetime.now()
        f = request.FILES.get("file")
        file_content = ContentFile(f.read())
        pid = request.POST.get("pid")
        uid = request.user.id
        verify = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        sided = request.POST.get("sided")
        number_up = request.POST.get("number_up")
        number_up_layout = request.POST.get("number_up_layout")
        media = request.POST.get("media")
        page_ranges = request.POST.get("page_range")
        copies = request.POST.get("copies")
        created_time = datetime.datetime.now()
        order = PrintJobs.objects.create()
        status = 1
        order = PrintJobs.objects.create(pid=pid,uid=uid,verify=verify,sided=sided,number_up=number_up,number_up_layout=number_up_layout,media=media,copies=copies,page_ranges=page_ranges,created_time=created_time)
        order.upload.save(f.name,file_content)
        file_pages = getPDFPages(order.upload.path)
        order.file_pages=file_pages
        order.cost = file_pages * 0.5 * 1/sided

    return render(request, 'user/print/new.html', locals())


def pay_order(request):
    if request.method == 'POST':
        pass

    return render(request, 'user/print/pay.html', locals())
