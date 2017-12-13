#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.
from .models import Profile, BalanceLog, Printer, PrinterOptions, RedeemCode, PrintJobs, paysAPI, Order


admin.site.register(Profile)
admin.site.register(BalanceLog)
admin.site.register(Printer)
admin.site.register(PrinterOptions)
admin.site.register(PrintJobs)
admin.site.register(RedeemCode)
admin.site.register(Order)
admin.site.register(paysAPI)
