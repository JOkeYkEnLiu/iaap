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
        'loginForm': LoginForm(),
        'state': state,
    }

    return render(request, 'app/login.html', context)
