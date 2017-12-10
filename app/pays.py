#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import datetime

PAYSAPIUID = ""
PAYSAPITOKEN = ""

class paysAPI(object):
    """
    paysAPI 订单类, 传入orderuid, price, istype, orderid
    """
    
    def __init__(self, uid, price, istype, orderid):
        self.uid = PAYSAPIUID
        self.PAYSAPITOKEN = PAYSAPITOKEN
        self.RETURN_URL = "http://print.iaa.ink:58000/user/print/return"
        self.NOTIFY_URL = "http://print.iaa.ink:58000/notify_url"
        self.orderuid = uid
        self.price = price
        self.istype = istype
        self.orderid = orderid
        self.key = hashlib.md5((str(self.istype) + str(self.NOTIFY_URL) + str(self.orderid) + str(self.orderuid) +
                                str(self.price) + str(self.RETURN_URL) + str(self.PAYSAPITOKEN) + str(self.uid)).encode("utf-8")).hexdigest()


class paysAPIReturn(object):
    """
    paysAPI 返回类
    """

    def __init__(self,paysapi_id,orderid,price,realprice,orderuid,key):
        self.token = PAYSAPITOKEN
        self.paysapi_id = paysapi_id
        self.orderid = orderid
        self.price = price
        self.realprice = realprice
        self.orderuid = orderuid
        self.key = key
    
    def validateKEY(self):
        self.myKEY = hashlib.md5((self.orderid + self.orderuid + self.paysapi_id +
                                  self.price + self.realprice + self.token).encode("utf-8")).hexdigest()
        if self.myKEY == self.key:
            return True
        else:
            return False
