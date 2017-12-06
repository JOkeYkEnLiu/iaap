from .models import Profile, BalanceLog, Printer, PrinterOptions, RedeemCode, User, PrintJobs, paysAPI
import math

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
    pass

def doPrint(order):
    pid = order.pid
    printer = Printer.objects.get(id=pid)

    run = printer.command + " " + printer.device_name

    if printer.host_name:
        run = run + " " + printer.host_name + ":" + printer.port
    if printer.username:
        run = run + " " + printer.username
    
    run = run + " " + printer.media + " " + order.media
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
    run = run + " " +printer.copies + " " + order.copies
    print(run)
    afterPrint(order)