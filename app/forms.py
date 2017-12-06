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

    def __init__(self, *args, **kwargs):

        self.fields['upload'].widget.attrs['class']='form-control m-input'
        self.fields['pid'].widget.attrs['class']='form-control m-input'
        self.fields['sided'].choices = [(1, "单面打印"), (2, "双面打印")]
        self.fields['sided'].attrs['class']='form-control m-input'
    
        self.fields['number_up'].attrs["type"] = "hidden"
        self.fields['number_up'].attrs["value"]= "1"
        self.fields['number_up_layout'].attrs["type"] = "hidden"
        self.fields['number_up_layout'].attrs["value"]= "tblr"
        self.fields['media'].attrs["type"]= "hidden"
        self.fields['media'].attrs["value"] = "A4"
        self.fields['page_ranges'].attrs["type"]= "hidden"
        self.fields['page_ranges'].attrs["value"] = ""

        self.fields['copies'].attrs['class']='form-control m-input'
        self.fields["copies"].attrs["type"]="number"
        self.fields["copies"].attrs["value"]=1
