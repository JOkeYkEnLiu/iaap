from .models import Profile, BalanceLog, Printer, PrinterOptions, RedeemCode, User, PrintJobs, paysAPI
import math
import os, datetime

def getCost(order):
    pid = order.pid
    cost_per_page = Printer.objects.get(id=pid).cost_per_page

    file_page = order.file_pages
    sided = order.sided
    number_up = order.number_up

    if sided == 1:
        p = 1
    elif sided>1:
        p = 0.5
    
    print_page = math.ceil(file_page * (1/number_up) * p)
    cost = cost_per_page * print_page
    return [print_page,cost]

def afterPrint(order):
    order.status = 0
    user = User.objects.get(id=order.uid)
    order.printed_time = datetime.datetime.now()
    order.save()
    balance = BalanceLog.objects.create(uid=order.uid,operator=order.uid,operation_time=order.printed_time,operation_type=0,balance_initial=user.profile.balance,balance_change=order.cost,balance_final=user.profile.balance-order.cost)
    balance.save()
    user.profile.balance = balance.balance_final
    user.save()

def doPrint(order):
    pid = order.pid
    printer = Printer.objects.get(id=pid)

    run = printer.command + " " + printer.device_name

    if printer.host_name:
        run = run + " " + printer.host_name + ":" + printer.port
    if printer.username:
        run = run + " " + printer.username
    
    run = run + " " + printer.media + order.media
    if order.sided == 1:
        sided = "one-sided"
    elif order.sided==2:
        sided = "two-sided-long-edge"
    else:
        sided = "two-sided-short-edge"
    run = run + " " + printer.sides + sided
    run = run + " " + printer.number_up + str(order.number_up) + " " + printer.number_up_layout + order.number_up_layout
    if order.page_ranges:
        run = run + " " + printer.page_ranges + " " + '"' + order.page_ranges + '"'
    run = run + " " +printer.copies + " " + str(order.copies)
    run = run + " " + order.upload.path
    # os.system(run)
    print(run)
    afterPrint(order)

def beforePaysAPIPrint(order,paysAPIreturn):
    order.payment = 2
    order.status = 0
    order.printed_time = datetime.datetime.now()
    order.save()
    newPaysAPIreturn = paysAPI.objects.create(orderid=paysAPIreturn.orderid, uid=paysAPIreturn.uid, price=paysAPIreturn.price,
                                              realprice=paysAPIreturn.realprice, istype=paysAPIreturn.istype, paysapi_id=paysAPIreturn.paysapi_id, created_time=datetime.datetime.now())
    newPaysAPIreturn.save()
    doPaysAPIPrint(order)


def doPaysAPIPrint(order):
    pid = order.pid
    printer = Printer.objects.get(id=pid)

    run = printer.command + " " + printer.device_name

    if printer.host_name:
        run = run + " " + printer.host_name + ":" + printer.port
    if printer.username:
        run = run + " " + printer.username

    run = run + " " + printer.media + order.media
    if order.sided == 1:
        sided = "one-sided"
    elif order.sided == 2:
        sided = "two-sided-long-edge"
    else:
        sided = "two-sided-short-edge"
    run = run + " " + printer.sides + sided
    run = run + " " + printer.number_up + \
        str(order.number_up) + " " + \
        printer.number_up_layout + order.number_up_layout
    if order.page_ranges:
        run = run + " " + printer.page_ranges + " " + '"' + order.page_ranges + '"'
    run = run + " " + printer.copies + " " + str(order.copies)
    run = run + " " + order.upload.path
    # os.system(run)
    print(run)
