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
    operation_time = models.DateTimeField(help_text="操作时间")
    operation_type = models.IntegerField(choices=OPERATION_TYPES,default="变动类型")
    balance_initial = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="初始余额")
    balance_change = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="变动余额")
    balance_final = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="结束余额")

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
    status=models.IntegerField(choices=StatusChoices, help_text="打印机状态")

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

    # Metadata
    class Meta:
        ordering = ["-orderid"]

    # Methods
    def get_absolute_url(self):
         return reverse('job-detail', args=[str(self.id)])

    def __str__(self):
        return self.id


class RedeemCode(models.Model):
    """
    兑换码模型
    """

    # Fields
    code = models.CharField(max_length=128, help_text="兑换码")
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="金额")
    created_by = models.IntegerField(help_text="创建人")
    created_time = models.DateTimeField(help_text="创建时间")
    is_used = models.BooleanField(help_text="是否使用?")
    used_by = models.IntegerField(help_text="使用者（可选）", blank=True, null=True)
    used_time = models.DateTimeField(help_text="使用时间（可选）", blank=True, null=True)

    # Metadata
    class Meta:
        ordering = ["-created_time"]

    # Methods
    def get_absolute_url(self):
         return reverse('redeem-code-detail', args=[str(self.id)])

    def __str__(self):
        return self.code


class Order(models.Model):
    """
    订单模型
    """

    ORDER_TYPE_CHOICES = (
        (1,'打印'),
        (2,'充值'),
    )
    PAYMENT_CHOICES = (
        (1, '余额支付'),
        (2, 'paysAPI'),
        (99, '我是管理员'),
    )

    # Fields
    orderid = models.AutoField(primary_key=True, auto_created=True)
    order_type = models.IntegerField(choices=ORDER_TYPE_CHOICES,help_text='类型')
    uid = models.IntegerField(help_text="创建人")
    created_time = models.DateTimeField(help_text="创建时间")
    isPaid = models.BooleanField(help_text="是否付款")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="金额")
    payment = models.IntegerField(
        choices=PAYMENT_CHOICES, help_text="支付方式", blank=True, null=True)
    
    # Metadata
    class Meta:
        ordering = ["-created_time"]

    # Methods
    def get_absolute_url(self):
         return reverse('redeem-code-detail', args=[str(self.id)])

    def __str__(self):
        return self.orderid


class PrintJobs(models.Model):
    """
    打印任务模型
    """

    SIDED_CHOICES = (
        (1, '单面打印'),
        (2, '双面打印'),
        (3, '短边装订双面打印'),
    )
    STATUS_CHOICES = (
        (0, '已完成'),
        (1, '未完成'),
    )
    PID_CHOICES = (
        (1, '12F 的打印机'),
    )
    NUMBER_UP_LAYOUT_CHOICES = (
        ('tblr', '从上到下，从左到右'),
        ('tbrl', '从上到下，从右到左'),
        ('btlr', '从下到上，从左到右'),
        ('btrl', '从下到上，从右到左'),
    )
    # Fields
    order = models.OneToOneField(Orders)
    pid = models.IntegerField(
        choices=PID_CHOICES, help_text="所选打印机",)
    upload = models.FileField(upload_to='uploads', default="文件",)
    file_pages = models.IntegerField(help_text="文件页数", blank=True, null=True)
    verify = models.CharField(max_length=128, help_text="校验码",)
    sided = models.IntegerField(
        choices=SIDED_CHOICES, help_text='双面打印选项',)
    number_up = models.IntegerField(help_text="每张页数", default=1,)
    number_up_layout = models.CharField(
        max_length=128, choices=NUMBER_UP_LAYOUT_CHOICES, help_text="布局")
    media = models.CharField(max_length=128, help_text="介质",)
    page_ranges = models.CharField(
        max_length=128, help_text="页面范围", blank=True, null=True)
    copies = models.IntegerField(help_text="份数", default=1)
    print_pages = models.IntegerField(
        help_text="实际打印张数", blank=True, null=True)
    cost = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="花费", blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, help_text="任务状态")
    printed_time = models.DateTimeField(
        help_text="任务打印时间（可选）", blank=True, null=True)


class paysAPI(models.Model):
    """
    paysAPI 调用日志模型
    """
    TYPE_CHOICES = (
        (1, '支付宝'),
        (2, '微信支付'),
    )
    order = models.OneToOneField(Orders)
    uid = models.IntegerField(help_text="用户")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="价格")
    realprice = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="实际价格")
    istype = models.IntegerField(choices=TYPE_CHOICES, help_text='支付渠道')
    paysapi_id = models.TextField(
        help_text='paysAPI 订单号', blank=True, null=True)
    created_time = models.DateTimeField(help_text="创建时间")

    def __str__(self):
        return self.orderid
