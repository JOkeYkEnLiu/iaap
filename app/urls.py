#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib.staticfiles import views as static_views
from django.conf.urls.static import static
from django.conf import settings

import app.views as views

urlpatterns = [
                url(r'^$', views.index, name='index'),
                url(r'^about/', views.about, name='about'),
                url(r'^auth/login/', views.user_login, name='user_login'),
                url(r'^auth/logout/', views.user_logout, name='user_logout'),
                url(r'^auth/register/', views.user_register, name='user_register'),
                url(r'^auth/password_reset/', views.password_reset, name='password_reset'),
                url(r'^user/$', views.user_index, name='user'),
                url(r'^user/profile', views.profile, name='profile'),
                url(r'^user/code', views.code, name='code'),
                url(r'^user/print/$', views.print_index, name='print_index'),
                url(r'^user/announcement', views.announcement, name='announcement'),
                url(r'^static/(?P<path>.*)$', static_views.serve, name='static'),
            ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
