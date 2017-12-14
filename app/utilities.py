from .models import Profile, BalanceLog, Printer, PrinterOptions, RedeemCode, User, PrintJobs, paysAPI, Order
import math
import os, datetime

def getCost(print_job):
    pid = print_job.pid
    cost_per_page = Printer.objects.get(id=pid).cost_per_page

    file_page = print_job.file_pages
    sided = print_job.sided
    number_up = print_job.number_up

    if sided == 1:
        p = 1
    elif sided>1:
        p = 0.5
    
    print_page = math.ceil(file_page * (1/number_up) * p)
    cost = cost_per_page * print_page
    return [print_page,cost]

def afterPrint(print_job):
    print_job.status = 0
    user = User.objects.get(id=print_job.order.uid)
    print_job.printed_time = datetime.datetime.now()
    print_job.order.isPaid = 1
    print_job.save()
    balance = BalanceLog.objects.create(uid=print_job.order.uid,operator=print_job.order.uid,operation_time=print_job.printed_time,operation_type=0,balance_initial=user.profile.balance,balance_change=print_job.cost,balance_final=user.profile.balance-print_job.cost)
    balance.save()
    user.profile.balance = balance.balance_final
    user.save()

def doPrint(print_job):
    pid = print_job.pid
    printer = Printer.objects.get(id=pid)

    run = printer.command + " " + printer.device_name

    if printer.host_name:
        run = run + " " + printer.host_name + ":" + printer.port
    if printer.username:
        run = run + " " + printer.username
    
    run = run + " " + printer.media + print_job.media
    if print_job.sided == 1:
        sided = "one-sided"
    elif print_job.sided==2:
        sided = "two-sided-long-edge"
    else:
        sided = "two-sided-short-edge"
    run = run + " " + printer.sides + sided
    run = run + " " + printer.number_up + str(print_job.number_up) + " " + printer.number_up_layout + print_job.number_up_layout
    if print_job.page_ranges:
        run = run + " " + printer.page_ranges + " " + '"' + print_job.page_ranges + '"'
    run = run + " " +printer.copies + " " + str(print_job.copies)
    run = run + " " + print_job.upload.path
    # os.system(run)
    print(run)
    afterPrint(print_job)

def beforePaysAPIPrint(print_job,paysAPIreturn):
    print_job.order.payment = 2
    print_job.status = 0
    print_job.printed_time = datetime.datetime.now()
    print_job.order.isPaid = 1
    print_job.save()
    newPaysAPIreturn = paysAPI.objects.create(order=print_job.order, uid=paysAPIreturn.uid, price=paysAPIreturn.price,
                                              realprice=paysAPIreturn.realprice, istype=paysAPIreturn.istype, paysapi_id=paysAPIreturn.paysapi_id, created_time=datetime.datetime.now())
    newPaysAPIreturn.save()
    doPaysAPIPrint(print_job)


def doPaysAPIPrint(print_job):
    pid = print_job.pid
    printer = Printer.objects.get(id=pid)

    run = printer.command + " " + printer.device_name

    if printer.host_name:
        run = run + " " + printer.host_name + ":" + printer.port
    if printer.username:
        run = run + " " + printer.username

    run = run + " " + printer.media + print_job.media
    if print_job.sided == 1:
        sided = "one-sided"
    elif print_job.sided == 2:
        sided = "two-sided-long-edge"
    else:
        sided = "two-sided-short-edge"
    run = run + " " + printer.sides + sided
    run = run + " " + printer.number_up + \
        str(print_job.number_up) + " " + \
        printer.number_up_layout + print_job.number_up_layout
    if print_job.page_ranges:
        run = run + " " + printer.page_ranges + " " + '"' + print_job.page_ranges + '"'
    run = run + " " + printer.copies + " " + str(print_job.copies)
    run = run + " " + print_job.upload.path
    # os.system(run)
    print(run)
