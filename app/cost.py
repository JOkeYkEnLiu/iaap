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

