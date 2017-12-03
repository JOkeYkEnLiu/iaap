# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-02 16:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_printer'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrinterOptions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.IntegerField(help_text='打印机')),
                ('function', models.CharField(help_text='功能', max_length=128)),
                ('value', models.CharField(help_text='选项', max_length=128)),
                ('description', models.CharField(help_text='描述', max_length=128)),
                ('is_active', models.BooleanField(help_text='是否启用?')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='PrintJobs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.IntegerField(help_text='所选打印机')),
                ('uid', models.IntegerField(help_text='用户')),
                ('upload', models.FileField(default='文件', upload_to='uploads/%Y/%m/%d/')),
                ('file_pages', models.IntegerField(help_text='文件页数')),
                ('verify', models.CharField(help_text='校验码', max_length=128)),
                ('sided', models.IntegerField(help_text='1 为单面打印双面打印，2 为长边装订双面打印，3 为短边装订双面打印')),
                ('number_up', models.IntegerField(default=1, help_text='每张页数')),
                ('number_up_layout', models.CharField(help_text='介质', max_length=128)),
                ('page_ranges', models.CharField(help_text='页面范围', max_length=128)),
                ('copies', models.IntegerField(default=1, help_text='份数')),
                ('print_pages', models.IntegerField(help_text='实际打印张数')),
                ('cost', models.DecimalField(decimal_places=2, help_text='花费', max_digits=10)),
                ('created_time', models.TimeField(help_text='任务创建时间')),
                ('is_printed', models.BooleanField(help_text='是否打印?')),
                ('printed_time', models.TimeField(blank=True, help_text='任务打印时间（可选）', null=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='RedeemCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(help_text='兑换码', max_length=128)),
                ('amount', models.DecimalField(decimal_places=2, help_text='金额', max_digits=10)),
                ('created_by', models.IntegerField(help_text='创建人')),
                ('created_time', models.TimeField(help_text='创建时间')),
                ('is_used', models.BooleanField(help_text='是否使用?')),
                ('used_by', models.IntegerField(blank=True, help_text='使用者（可选）', null=True)),
                ('used_time', models.TimeField(blank=True, help_text='使用时间（可选）', null=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.AlterField(
            model_name='printer',
            name='host_name',
            field=models.CharField(blank=True, help_text='主机名（可选）', max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='printer',
            name='port',
            field=models.IntegerField(blank=True, help_text='端口（可选）', null=True),
        ),
        migrations.AlterField(
            model_name='printer',
            name='username',
            field=models.CharField(blank=True, help_text='用户名（可选）', max_length=128, null=True),
        ),
    ]
