#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Used to generate URLs by reversing the URL patterns
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=0.00)


    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Printer(models.Model):
    """
    打印机模型
    """

    # Fields
    printer_name = models.CharField(max_length=128, help_text="打印机名称")
    command = models.CharField(max_length=128, help_text="打印命令", default="lp")
    device_name = models.CharField(max_length=128, help_text="设备名称")
    host_name = models.CharField(max_length=128, help_text="主机名", Blank=True)
    port = models.IntegerField(help_text="端口", Blank=True)
    username = models.CharField(max_length=128, help_text="用户名", Blank=True)
    media = models.CharField(max_length=128, help_text="介质命令")
    sides = models.CharField(max_length=128, help_text="双面打印命令")
    number_up = models.CharField(max_length=128, help_text="每页张数命令")
    number_up_layout = models.CharField(max_length=128, help_text="布局命令")
    page_ranges = models.CharField(
        max_length=128, help_text="页面范围命令")
    copies = models.CharField(max_length=128, help_text="份数命令")
    cost_per_page = models.DecimalField(max_digits=10,decimal_places=2, help_text="每页花费", default="0.50")

    # Metadata
    class Meta:
        ordering = ["-id"]

    # Methods
    def get_absolute_url(self):
         return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        return self.printer_name
