#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.
from .models import Profile, Printer, PrinterOptions, PrintJobs, RedeemCode


admin.site.register(Profile)
admin.site.register(Printer)
admin.site.register(PrinterOptions)
admin.site.register(PrintJobs)
admin.site.register(RedeemCode)
