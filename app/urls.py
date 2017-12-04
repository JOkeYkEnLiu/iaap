#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib.staticfiles import views as static_views
from django.conf.urls.static import static
from django.conf import settings

import app.views as views

from django.conf.urls import handler404, handler500


handler404 = views.page_error
handler500 = views.page_error

urlpatterns = [
                url(r'^$', views.index, name='index'),
                url(r'^redirect/', views.redirect_url, name='redirect_url'),
                url(r'^about/', views.about, name='about'),
                url(r'^auth/login/', views.user_login, name='user_login'),
                url(r'^auth/logout/', views.user_logout, name='user_logout'),
                # url(r'^auth/register/', views.user_register, name='user_register'),
                # url(r'^auth/password_reset/', views.password_reset, name='password_reset'),
                url(r'^user/$', views.user_index, name='user'),
                url(r'^user/index$', views.user_index, name='user'),
                url(r'^user/profile', views.profile, name='profile'),
                # url(r'^user/pay/code', views.code, name='code'),
                # url(r'^user/pay/log', views.pay_log, name='pay_log'),
                # url(r'^user/pay/online', views.online_pay, name='online_pay'),
                # url(r'^user/print/$', views.print_index, name='print_index'),
                # url(r'^user/print/new', views.new_print_job, name='new_print_job'),
                # url(r'^user/printer/$', views.view_printers, name='view_printers'),
                # url(r'^user/ticket/$', views.ticket, name='ticket'),
                # url(r'^user/ticket/new', views.new_ticket, name='new_ticket'),
                # url(r'^user/FAQ', views.FAQ, name='FAQ'),
                url(r'^static/(?P<path>.*)$', static_views.serve, name='static'),
            ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
