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
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="账户余额")


    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class BalanceLog(models.Model):
    """
    余额变动模型
    """
    OPERATION_TYPES = (
        (0, '打印扣费'),
        (1, '兑换码充值'),
        (2, '微信充值'),
        (3, '支付宝充值'),
        (4, '后台修改'),
    )

    # Fields
    uid = models.IntegerField(help_text="用户")
    operator = models.IntegerField(help_text="操作者")
    operation_time = models.TimeField(help_text="操作时间")
    operation_type = models.IntegerField(choices=OPERATION_TYPES,default="变动类型")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="初始余额")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="变动余额")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="结束余额")

    # Metadata

    class Meta:
        ordering = ["-id"]

    # Methods
    def get_absolute_url(self):
         return reverse('balance-log-detail', args=[str(self.id)])

    def __str__(self):
        return "%s 的余额变动" % (User.objects.get(pk=self.uid).username)

class Printer(models.Model):
    """
    打印机模型

    """

    StatusChoices = (
        (0, '正常打印'),
        (2, '漏墨'),
        (10, '打印机未连接'),
        (11, '缺纸'),
        (12, '缺墨'),
    )


    # Fields
    printer_name = models.CharField(max_length=128, help_text="打印机名称")
    command = models.CharField(max_length=128, help_text="打印命令", default="lp")
    device_name = models.CharField(max_length=128, help_text="设备名称")
    host_name = models.CharField(max_length=128, help_text="主机名（可选）", blank=True, null=True)
    port = models.IntegerField(help_text="端口（可选）", blank=True, null=True)
    username = models.CharField(
        max_length=128, help_text="用户名（可选）", blank=True, null=True)
    media = models.CharField(max_length=128, help_text="介质命令")
    sides = models.CharField(max_length=128, help_text="双面打印命令")
    number_up = models.CharField(max_length=128, help_text="每页张数命令")
    number_up_layout = models.CharField(max_length=128, help_text="布局命令")
    page_ranges = models.CharField(
        max_length=128, help_text="页面范围命令")
    copies = models.CharField(max_length=128, help_text="份数命令")
    cost_per_page = models.DecimalField(max_digits=10,decimal_places=2, help_text="每页花费", default="0.50")
    status=model.IntegerField(choices=StatusChoices, help_text="打印机状态")

    # Metadata
    class Meta:
        ordering = ["-id","status"]

    # Methods
    def get_absolute_url(self):
         return reverse('printer-detail', args=[str(self.id)])

    def __str__(self):
        return self.printer_name


class PrinterOptions(models.Model):
    """
    打印机选项模型
    """

    # Fields
    pid = models.IntegerField(help_text="打印机")
    function = models.CharField(max_length=128, help_text="功能")
    value = models.CharField(max_length=128, help_text="选项")
    description = models.CharField(max_length=128, help_text="描述")
    is_active = models.BooleanField(help_text="是否启用?")
    # Metadata
    class Meta:
        ordering = ["-id"]

    # Methods
    def get_absolute_url(self):
         return reverse('printer-option-detail', args=[str(self.id)])

    def __str__(self):
        return self.description


class PrintJobs(models.Model):
    """
    打印任务模型
    """

    SIDED_CHOICES = (
        (1, '单面打印'),
        (2, '长边装订双面打印'),
        (3, '短边装订双面打印'),
    )

    # Fields
    pid = models.IntegerField(help_text="所选打印机")
    uid = models.IntegerField(help_text="用户")
    upload = models.FileField(upload_to='uploads/%Y/%m/%d/', default="文件")
    file_pages = models.IntegerField(help_text="文件页数")
    verify = models.CharField(max_length=128, help_text="校验码")
    sided = models.IntegerField(choices=SIDED_CHOICES, help_text='双面打印选项')
    number_up = models.IntegerField(help_text="每张页数", default=1)
    number_up_layout = models.CharField(max_length=128, help_text="介质")
    page_ranges = models.CharField(max_length=128, help_text="页面范围")
    copies = models.IntegerField(help_text="份数", default=1)
    print_pages = models.IntegerField(help_text="实际打印张数")
    cost = models.DecimalField(max_digits=10, decimal_places=2, help_text="花费")
    created_time = models.TimeField(help_text="任务创建时间")
    is_printed = models.BooleanField(help_text="是否打印完成?")
    printed_time = models.TimeField(help_text="任务打印时间（可选）", blank=True, null=True)


    # Metadata
    class Meta:
        ordering = ["-id"]

    # Methods
    def get_absolute_url(self):
         return reverse('job-detail', args=[str(self.id)])

    def __str__(self):
        return "%s 创建的打印 %s 的任务"%(User.objects.get(pk=self.uid).username, self.upload)


class RedeemCode(models.Model):
    """
    兑换码模型
    """

    # Fields
    code = models.CharField(max_length=128, help_text="兑换码")
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="金额")
    created_by = models.IntegerField(help_text="创建人")
    created_time = models.TimeField(help_text="创建时间")
    is_used = models.BooleanField(help_text="是否使用?")
    used_by = models.IntegerField(help_text="使用者（可选）", blank=True, null=True)
    used_time = models.TimeField(help_text="使用时间（可选）", blank=True, null=True)

    # Metadata
    class Meta:
        ordering = ["-id"]

    # Methods
    def get_absolute_url(self):
         return reverse('redeem-code-detail', args=[str(self.id)])

    def __str__(self):
        return self.amount


