#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from app.models import PrintJobs


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=16,
        widget=forms.TextInput(attrs={
            'class': 'form-control m-input',
            'name': 'username',
            'id': 'id_username',
            "placeholder":"用户名"
        }, ),required=True, )
    password = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control m-login__form-input--last',
            'type': 'password',
            'name': 'password',
            "placeholder":"密码",
        }, ),required=True,
    )
    remember = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'class': 'form-control m-input',
            'type': 'checkbox',
            'name': 'remember',
        }),
    )


class RegisterForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control m-input',
            'name': 'username',
            "placeholder":"用户名"
        },),required=True,
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control m-input',
            'name': 'email',
            "type":"email",
            "placeholder":"邮箱"
        },),required=True,
    )
    password = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control m-input',
            'name': 'password',
            "placeholder":"密码"
        },),required=True,
    )
    re_password = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control m-input m-login__form-input--last',
            'type': 'password',
            'name': 'repeat_password',
            "placeholder":"确认密码"
        }, ),required=True,
    )


class QuickNewOrderForm(forms.Form):
    SIDED_CHOICES = (
        (1, '单面打印'),
        (2, '双面打印'),
        (3, '短边装订双面打印'),
    )
    PID_CHOICES = (
        (1, '12F 的打印机'),
    )
    upload = forms.FileField(widget=forms.FileInput(
        attrs={'class': 'form-control m-input'}))
    pid = forms.IntegerField(widget=forms.Select(choices=PID_CHOICES, attrs={
                             'class': 'form-control m-input', "value": "1"}))
    sided = forms.IntegerField(widget=forms.Select(choices=SIDED_CHOICES, attrs={
                               'class': 'form-control m-input', "value": "1"}))
    number_up = forms.IntegerField(widget=forms.NumberInput(
        attrs={"type": "hidden", "value": 1}))
    number_up_layout = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={"type": "hidden", "value": "tblr"}))
    media = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={"type": "hidden", "value": "A4"}))
    page_range = forms.CharField(required=False, max_length=128, widget=forms.TextInput(
        attrs={"type": "hidden", "value": ""}))
    copies = forms.IntegerField(min_value=1,widget=forms.NumberInput(
        attrs={'class': 'form-control m-input', "type": "number", "value": 1,"min": 1}))


class NewOrderForm(forms.Form):
    SIDED_CHOICES = (
        (1, '单面打印'),
        (2, '双面打印'),
        (3, '短边装订双面打印'),
    )
    PID_CHOICES = (
        (1, '12F 的打印机'),
    )
    NUMBERUP_CHOICES = (
        (1, '每张 1 页'),
        (2, '每张 2 页'),
        (4, '每张 4 页'),
        (6, '每张 6 页'),
        (9, '每张 9 页'),
        (16, '每张 16 页'),
    )
    NUMBERUPLAYOUT_CHOICES = (
        ('tblr', '从上到下，从左到右'),
        ('tbrl', '从上到下，从右到左'),
        ('btlr', '从下到上，从左到右'),
        ('btrl', '从下到上，从右到左'),
    )
    MEDIA_CHOICES = (
        ('A4', 'A4'),
    )
    upload = forms.FileField(widget=forms.FileInput(
        attrs={'class': 'form-control m-input'}))
    pid = forms.IntegerField(widget=forms.Select(choices=PID_CHOICES, attrs={
                             'class': 'form-control m-input', "value": "1"}))
    sided = forms.IntegerField(widget=forms.Select(choices=SIDED_CHOICES, attrs={
                               'class': 'form-control m-input', "value": "1"}))
    number_up = forms.IntegerField(widget=forms.Select(choices=NUMBERUP_CHOICES, attrs={
        'class': 'form-control m-input', "value": "1"}))
    number_up_layout = forms.CharField(widget=forms.Select(choices=NUMBERUPLAYOUT_CHOICES, attrs={
        'class': 'form-control m-input', "value": "tblr"}))
    media = forms.CharField(widget=forms.Select(choices=MEDIA_CHOICES, attrs={
        'class': 'form-control m-input', "value": "A4"}))
    page_range = forms.CharField(required=False, max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control m-input', "value": ""}))
    copies = forms.IntegerField(min_value=1, widget=forms.NumberInput(
        attrs={'class': 'form-control m-input', "type": "number", "value": 1, "min": 1}))

class BalanceRechargeForm(forms.Form):
    # price = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.)
    pass