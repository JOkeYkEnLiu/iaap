#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django import forms
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.files.base import ContentFile

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from .models import Profile, BalanceLog, Printer, PrinterOptions, RedeemCode, User, PrintJobs, paysAPI, Order
from app.pays import paysAPI, paysAPIReturn
from app.pdf_page_count import getPDFPages
from app.forms import QuickNewOrderForm
from app.utilities import getCost, doPrint, beforePaysAPIPrint
import random
import string, hashlib

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
    if request.method=="POST":
        form = QuickNewOrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = Order(order_type = 1,
                          uid = request.user.id,
                          created_time = datetime.datetime.now(),
                          isPaid = 0,
                          price = 0.00,
                          payment = 1,
                          )
            order.save()
            print_job = PrintJobs(order=order,
                                  pid=form.cleaned_data['pid'],
                                  upload=request.FILES['upload'],
                                  verify=''.join(random.sample(string.ascii_letters + string.digits, 8)),
                                  sided=form.cleaned_data['sided'],
                                  number_up=form.cleaned_data['number_up'],
                                  number_up_layout=form.cleaned_data['number_up_layout'],
                                  media=form.cleaned_data['media'],
                                  page_ranges=form.cleaned_data['page_range'],
                                  copies=form.cleaned_data['copies'],
                                  print_pages=0,
                                  cost=0,
                                  status=1,
                                )
            print_job.save()
            print_job.file_pages = getPDFPages(print_job.upload.path)
            print_job.save()
            cost=getCost(print_job)
            print_job.print_pages=cost[0]
            print_job.cost=cost[1]
            print_job.order.price = cost[1]
            print_job.save()
            return HttpResponseRedirect('/user/print/pay?orderid=%s&verify=%s'%(str(order.orderid),str(print_job.verify)))

    else:
        if request.GET.get('orderid'):
            form = QuickNewOrderForm(initial={"pid": 1, "sided": 1})
        else:
            form = QuickNewOrderForm(initial={"pid":1,"sided":1})
    return render(request, 'user/print/new.html', locals())


@login_required
def pay_order(request):
    if request.GET.get('orderid'):
        print_job = PrintJobs.objects.get(order=Order.objects.get(orderid=request.GET.get('orderid')))
        user = request.user
        if print_job.sided == 1:
            sided = "单面打印"
        elif print_job.sided >1 :
            sided = "双面打印"
        if print_job.pid == 1:
            printer = "12F 的打印机"
        paysAPIWeChat = paysAPI(uid=request.user.id, price=print_job.cost, istype=2, orderid=print_job.order.orderid)
        paysAPIAli = paysAPI(uid=request.user.id, price=print_job.cost,istype=1, orderid=print_job.order.orderid)
    else:
        return HttpResponseRedirect('/user/print/new')

    return render(request, 'user/print/pay.html', locals())


@csrf_exempt
def notify_return(request):
    if request.method == "POST":
        paysapi_id = request.POST.get("paysapi_id")
        orderid = request.POST.get("orderid")
        price = request.POST.get("price")
        realprice = request.POST.get("realprice")
        orderuid = request.POST.get("orderuid")
        key = request.POST.get("key")
        paysAPIreturn = paysAPIReturn(
            paysapi_id=paysapi_id, orderid=orderid, price=price, realprice=realprice, orderuid=orderuid, key=key)
        if (paysapi_id and orderid and price and realprice and orderuid and key):
            print('有效')
            if paysAPIreturn.validateKEY():
                beforePaysAPIPrint(PrintJobs.objects.get(order=Order.objects.get(orderid=orderid)),paysAPIreturn)
                return HttpResponse("收到")
            else:
                print('key 无效')
        else:
            print('无效')

@login_required
def print_return(request):
    if request.method == "POST":
        orderid = request.POST.get('orderid')
        if orderid:
            verify = request.POST.get('verify')
            print_job = PrintJobs.objects.get(order=Order.objects.get(orderid=orderid))
            if verify == print_job.verify:
                if print_job.order.payment == 1:
                    if print_job.status == 1:
                        print_job = PrintJobs.objects.get(order=orderid)
                        doPrint(print_job)
                        state = "打印成功"
                        stateDetail = "如果打印机未能正常打印，请联系管理员。"
                        return render(request, 'user/message.html', locals())
                    else:
                        return HttpResponseRedirect('/user/print/new?orderid=%s'%orderid)
                else:
                    state = "错误码 101"
                    stateDetail = "如果您使用的是在线支付并且已经支付完成，打印机将正常打印。"
                    return render(request, 'user/message.html', locals())
            else:
                if print_job.order.payment == 2:
                    if print_job.status == 0:
                        state = "打印成功"
                        stateDetail = "如果打印机未能正常打印，请联系管理员。"
                        return render(request, 'user/message.html', locals())
                    else:
                        state = "错误码 102"
                        stateDetail = "您的订单很可能已经被打印，请联系管理员。"
                        return render(request, 'user/message.html', locals())
                else:
                    return HttpResponseRedirect('/user/print/new')
    else:
        return HttpResponseRedirect('/user/print/new')
