#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import datetime

class Orders(object):
    """
    订单类
    """

    def __init__(self):
        pass

class paysAPI(object):
    """
    paysAPI 订单类, 传入orderuid, price, istype, orderid
    """
    
    def __init__(self, orderuid, price, istype, orderid):
        self.PAYSAPIUID = ""
        self.PAYSAPITOKEN = ""
        self.RETURN_URL = ""
        self.NOTIFY_URL = ""
        self.orderuid = uid
        self.price = price
        self.istype = istype
        self.orderid = orderid
        self.key = md5.hexdigest()

    def generateKEY(self)
        md5 = hashlib.md5()
        md5.update(str(self.istype) + str(self.NOTIFY_URL) + str(self.orderid) + str(self.orderuid) +
                          str(self.price) + str(self.RETURN_URL) + str(self.PAYSAPITOKEN) + str(self.PAYSAPIUID))
