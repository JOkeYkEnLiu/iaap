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

class QuickNewOrderForm(forms.ModelForm):
    class Meta:
        model = PrintJobs
        fields=['upload','pid','sided','number_up','number_up_layout','media','page_ranges','copies']
        widgets = {
            'upload': forms.FileInput(attrs={'class': 'form-control m-input', }),
            "pid": forms.Select(choices=((1, "12F 的打印机")), attrs={'class': 'form-control m-input'}),
            'sided': forms.Select(choices=((1, "单面打印"), (2, "双面打印")), attrs={'class': 'form-control m-input'}),
            "number_up": forms.NumberInput(attrs={"type": "hidden", "value": 1}),
            "number_up_layout": forms.TextInput(attrs = {"type": "hidden", "value": "tblr"}),
            "media": forms.TextInput(attrs={"type": "hidden", "value": "A4"}),
            "page_ranges": forms.TextInput(attrs={"type": "hidden", "value": ""}),
            "copies": forms.NumberInput(attrs={'class': 'form-control m-input', "type": "number", "value": 1}),
            }
