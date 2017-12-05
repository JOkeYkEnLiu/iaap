#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=16,
        widget=forms.TextInput(attrs={
            'class': 'form-control m-input',
            'name': 'username',
            'id': 'id_username',
            "placeholder"="用户名"
        }, required=True,)
    )
    password = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control m-login__form-input--last',
            'type': 'password',
            'name': 'password',
            "placeholder"="密码",
        }, required=True,),
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
            "placeholder"="用户名"
        },required=True,),
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control m-input',
            'name': 'email',
            "type":"email",
            "placeholder"="邮箱"
        },required=True,),
    )
    password = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control m-input',
            'name': 'password',
            "placeholder"="密码"
        },required=True,),
    )
    re_password = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control m-input m-login__form-input--last',
            'type': 'password',
            'name': 'repeat_password',
            "placeholder"="确认密码"
        }, required=True,),
    )

