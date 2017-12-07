#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import datetime

class paysAPI(object):
    """
    paysAPI 订单类, 传入orderuid, price, istype, orderid
    """
    
    def __init__(self, uid, price, istype, orderid):
        self.PAYSAPIUID = ""
        self.PAYSAPITOKEN = ""
        self.RETURN_URL = "http://print.iaa.ink/user/print/return"
        self.NOTIFY_URL = "http://print.iaa.ink/notify_url"
        self.orderuid = uid
        self.price = price
        self.istype = istype
        self.orderid = orderid
        self.key = hashlib.md5((str(self.istype) + str(self.NOTIFY_URL) + str(self.orderid) + str(self.orderuid) +
                                str(self.price) + str(self.RETURN_URL) + str(self.PAYSAPITOKEN) + str(self.PAYSAPIUID)).encode("utf-8")).hexdiges()

