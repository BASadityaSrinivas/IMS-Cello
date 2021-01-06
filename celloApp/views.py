from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from celloApp.forms import *
from celloApp.models import *
from django.urls import reverse
from sql import *
from csvWrite import *
import os
from os import listdir
from os.path import isfile, join
import json, logging, socket, datetime

## First time
# CelloTypes.objects.get_or_create(color='White', quantityInStock=0)
# CelloTypes.objects.get_or_create(color='Brown', quantityInStock=0)
# CelloTypes.objects.get_or_create(color='Other', quantityInStock=0)
# loginTable.objects.get_or_create(pk=1, userN='', passW='')

## Always
usersTable.objects.get_or_create(pk=1, userNames='bas', passwords='bas')
loginTable.objects.filter(pk=1).update(userN='', passW='')
tempTableProcess.objects.all().delete()
tempTableOrder.objects.all().delete()

logger = logging.getLogger('django')
logger.warning("\n-------------------------------------------------------------")
logger.warning("\nLogged In By \n--------------------------------------------------\nHost name : {} \nIP Address : {}\n--------------------------------------------------".format(socket.gethostname(), socket.gethostbyname(socket.gethostname())))


def chkLogin():
    if(loginTable.objects.values_list('userN')[0][0]=='' and loginTable.objects.values_list('passW')[0][0]==''):
        return False
    else:
        return True


def index(request):
    raw = CelloTypes.objects.all()
    process = Processed.objects.order_by('color', 'length')
    orderTableInP = OrderTable.objects.order_by('oID').filter(status__in=['In Progress', 'New'])
    orderTableNP = OrderTable.objects.order_by('oID').filter(payment__exact='Not Paid').exclude(status__exact="Abandoned")
    ProcessForm = ProcessedForm
    CustEditFormSta = CustomerEditFormStatus
    CustomerEditFormPay = CustomerEditFormPayment

    qua = 0
    flag = 0
    url = request.build_absolute_uri()  # to know absolute url

    if (chkLogin()==False):
        return HttpResponseRedirect(reverse('login'))

    if request.method == 'POST':
        if request.POST.get('addProcess'):
            processTableItems = {}
            form = ProcessForm(request.POST)
            col = form['color'].value()
            len = form['length'].value()
            wid = form['width'].value()
            qua = form['quantity'].value()
            dat = form['date'].value()
            if form.is_valid():
                usedJumbo = form.cleaned_data.get("usedJumbo")

            if qua=='0':
                flag = 1
                messages.success(request, "Quantity is Zero, so not added")
            else:
                param = (len, wid, col, qua, dat)

                processTableItems['date'] = dat
                processTableItems['color'] = col
                processTableItems['length'] = len
                processTableItems['width'] = wid
                processTableItems['quantity'] = qua
                processTableItems['usedJumbo'] = ''

                if(tempTableProcess.objects.values_list('pk')):
                    for num in tempTableProcess.objects.values_list('pk'):
                        n = num[0]
                else:
                    n = 0

                tempTableProcess.objects.create(pk=int(n)+1, order=processTableItems)

                flag = 1
                messages.success(request, "Added in Processed Successful")
                logger.warning(">>>>> PROCESSED ADD : >>>>> Added {} , {} , {} : {}".format(col, len, wid, qua))

        elif request.POST.get('delProcess'):
            form = ProcessForm(request.POST)
            col = form['color'].value()
            len = form['length'].value()
            wid = form['width'].value()
            if (Processed.objects.values_list('quantity').filter(color__exact=col, length=len, width=wid)):qua = Processed.objects.values_list('quantity').filter(color__exact=col, length=len, width=wid)[0][0]
            param = (len, wid, col)
            ProcessDel(param)
            paramProcess = (datetime.date.today(), 'Deleted', '', qua, col,wid, len)
            appendProcessed(paramProcess)
            flag = 1
            messages.success(request, "Deleted in Processed Successful")
            logger.warning(">>>>> PROCESSED DEL : >>>>> Deleted {} , {} , {} ".format(col, len, wid))

        elif request.POST.get('addUsedJumbo'):
            processTableItems = {}

            form = ProcessForm(request.POST)
            if form.is_valid():
                col = form.cleaned_data.get("usedJumboColor")
                usedJumbo = form.cleaned_data.get("usedJumbo")

            if usedJumbo==0:
                flag = 1
                messages.success(request, "Quantity is Zero, so not added")
            else:
                processTableItems['date'] = ''
                processTableItems['color'] = col
                processTableItems['length'] = ''
                processTableItems['width'] = ''
                processTableItems['quantity'] = ''
                processTableItems['usedJumbo'] = usedJumbo

                if(tempTableProcess.objects.values_list('pk')):
                    for num in tempTableProcess.objects.values_list('pk'):
                        n = num[0]
                else:
                    n = 0

                tempTableProcess.objects.create(pk=int(n)+1, order=processTableItems)

                flag = 1
                messages.success(request,"Added the Jumbo in Processed Successful")

        elif request.POST.get('clrProcessItems'):
            flag = 1
            tempTableProcess.objects.all().delete()
            messages.success(request, "Process Basket cleared")

        elif request.POST.get('AddProcessedToTable'):
            processTableItems = {}
            if(tempTableProcess.objects.values_list('pk')):
                for num in tempTableProcess.objects.values_list('pk', 'order'):
                    n1 = num[0]
                    processTableItems[n1] = ast.literal_eval(num[1])

            dict = processTableItems

            jumbo = CelloTypes.objects.values_list('quantityInStock')

            for items in dict:  # For tabulation
                if dict[items]['length'] == '':
                    if dict[items]['color'] == 'White':
                        if dict[items]['usedJumbo'] > jumbo[0][0]:
                            messages.success(request, "Inadequate Jumbos")
                            return HttpResponseRedirect(url)

                    elif dict[items]['color'] == 'Brown':
                        if dict[items]['usedJumbo'] > jumbo[1][0]:
                            messages.success(request, "Inadequate Jumbos")
                            return HttpResponseRedirect(url)

                    elif dict[items]['color'] == 'Other':
                        if dict[items]['usedJumbo'] > jumbo[2][0]:
                            messages.success(request, "Inadequate Jumbos")
                            return HttpResponseRedirect(url)

            if path.isfile("csvFiles/entry.csv") == False:
                createEntry()

            # For findig the SNo
            n = 0
            with open('csvFiles/entry.csv', newline='') as entryReadFile:
                reader = csv.DictReader(entryReadFile)
                for row in reader:
                    if row['SNo'] != '':
                        n = row['SNo']
                entryReadFile.close()

            with open('csvFiles/entry.csv', 'a+',
                      newline='') as entryWriteFile:
                writer = csv.writer(entryWriteFile)
                m = int(n) + 1
                writer.writerow((m, '', '', '', ''))
                entryWriteFile.close()

            for items in dict:  # For tabulation
                if dict[items]['length'] != '':
                    param = (dict[items]['length'],
                             dict[items]['width'], dict[items]['color'],
                             int(dict[items]['quantity']), dict[items]['date'])
                    ProcessAdd(param)
                elif dict[items]['length'] == '':
                    param = (dict[items]['color'], dict[items]['usedJumbo'],
                             '')
                    processUsedJumbo(dict[items]['color'],
                                     dict[items]['usedJumbo'])

            for items in dict:  # For CSV
                if dict[items]['length'] != '':  # Processed tapes
                    desc = str(dict[items]['color'] + '-' +
                               dict[items]['length'] + '-' +
                               dict[items]['width'])
                    paramEntry = (dict[items]['date'], desc,
                                  dict[items]['quantity'], '')
                    # paramProcess = (date,desc,quantity,color,width,length)
                    paramProcess = (dict[items]['date'], 'Created',
                                    int(dict[items]['quantity']), '',
                                    dict[items]['color'], dict[items]['width'],
                                    dict[items]['length'])
                    appendProcessed(paramProcess)
                    appendEntry(paramEntry)

                elif dict[items]['length'] == '':  # Used Jumbos
                    desc = str(dict[items]['color'] + ' Jumbo')
                    param = (dict[items]['date'], desc, '',
                             dict[items]['usedJumbo'])
                    appendJumbo(
                        (str(datetime.date.today()),
                         'Process ' + dict[items]['color'], '',
                         dict[items]['usedJumbo'], dict[items]['color']))
                    appendEntry(param)

            tempTableProcess.objects.all().delete()
            flag = 1
            messages.success(request, "Process Basket cleared")

        elif request.POST.get('editCustSta'):
            form = CustomerEditFormStatus(request.POST)
            oId = form['oID'].value()
            sta = form['status'].value()
            pay = "Nothing"
            cId = eval(oId)[0]
            param = (cId, pay)
            payChk = OrderTable.objects.values_list('payment').filter(
                oID__exact=str(cId))[0][0]

            oldPay = OrderTable.objects.values_list('payment').filter(
                oID__exact=str(cId))[0][0]
            oldSta = OrderTable.objects.values_list('status').filter(
                oID__exact=str(cId))[0][0]

            if oldSta != sta:
                if sta == "In Progress":
                    msg = InProgressOrder(param)
                    flag = 1
                    messages.success(request, msg)
                    logger.warning(
                        ">>>>> CUSTOMER EDIT PAYMENT : >>>>> Edited Status {} : {}"
                        .format(cId, pay))

                elif sta == "Abandoned":
                    if oldSta == "Completed":
                        flag = 1
                        messages.success(request,
                                         "It is Completed, so can't Abandon")
                    elif payChk == "Not Paid":
                        msg = AbandonCustomer(param)
                        flag = 1
                        messages.success(request, msg)
                        logger.warning(
                            ">>>>> CUSTOMER ABANDONED : >>>>> Abandoned {} ".
                            format(cId))
                    else:
                        flag = 1
                        messages.success(request,
                                         "It is paid, so can't Abandon")

                elif sta == "Completed":
                    if oldSta == "Abandoned":
                        flag = 1
                        messages.success(request,
                                         "It is Abandoned, so can't Complete")
                    else:
                        msg = CompletedCustomer(param)
                        flag = 1
                        messages.success(request, msg)
                        logger.warning(
                            ">>>>> CUSTOMER COMPLETED : >>>>> Completed {} ".
                            format(cId))

        elif request.POST.get('editCustPay'):
            form = CustomerEditFormPayment(request.POST)
            oId = form['oID'].value()
            pay = form['payment'].value()
            cId = eval(oId)[0]
            param = (cId, pay)

            oldPay = OrderTable.objects.values_list('payment').filter(
                oID__exact=str(cId))[0][0]

            if oldPay != pay:
                msg = PaymentUpdate(param)
                flag = 1
                messages.success(request, msg)
                logger.warning(
                    ">>>>> CUSTOMER EDIT PAYMENT : >>>>> Edited Payment {} : {}"
                    .format(cId, pay))

        elif request.POST.get('logout'):
            loginTable.objects.filter(pk=1).update(userN='', passW='')
            return HttpResponseRedirect(reverse('login'))

        if flag != 1:
            messages.success(request, "Form submission Unsuccessful")

        return HttpResponseRedirect(url)

    processTableItemsDisplay = {}
    if(tempTableProcess.objects.values_list('pk')):
        for num in tempTableProcess.objects.values_list('pk', 'order'):
            n1 = num[0]
            processTableItemsDisplay[n1] = ast.literal_eval(num[1])

    context = {
        'raw': raw,
        'process': process,
        'ProcessForm': ProcessForm,
        'CustEditFormSta': CustEditFormSta,
        'CustEditFormPay': CustomerEditFormPay,
        'orderTableInP': orderTableInP,
        'orderTableNP': orderTableNP,
        'processTableItemsDisplay': processTableItemsDisplay
    }

    return render(request, 'celloApp/index.html', context)


def login(request):
    if request.method == 'POST':
        if request.POST.get('logout'):
            loginTable.objects.filter(pk=1).update(userN='', passW='')
            return HttpResponseRedirect(reverse('login'))

        userNform = request.POST['userName']
        passWform = request.POST['passWord']

        userNames = []
        passwords = []

        loginTable.objects.filter(pk=1).update(userN=userNform, passW=passWform)

        for usersFunc in usersTable.objects.values_list('userNames'):
            userNames.append(usersFunc[0])

        for usersFunc in usersTable.objects.values_list('passwords'):
            passwords.append(usersFunc[0])

        if (userNform in userNames and passWform in passwords):
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.success(request, "Wrong Credentials")

    return render(request, 'celloApp/login.html')


def customer(request):
    if (chkLogin()==False):
        return HttpResponseRedirect(reverse('login'))

    cust = CustomerMaster.objects.all()
    CustAdd = CustomerAddForm

    if request.method == 'POST':
        if request.POST.get('logout'):
            loginTable.objects.filter(pk=1).update(userN='', passW='')
            return HttpResponseRedirect(reverse('login'))

        elif request.POST.get('addCustomer'):
            form = CustomerAddForm(request.POST)
            param = (form['cName'].value(), form['address'].value(),
                     form['email'].value(), form['gstIN'].value())
            addCustomerNewTable(param)
            flag = 1
            messages.success(request, "Added to Customer table success")

        elif request.POST.get('exportCust'):
            response = HttpResponse(content_type='text/csv')

            writer = csv.writer(response)
            writer.writerow(['cID', 'Customer Name', 'Address', 'E-mail', 'GST IN'])
            for cust in CustomerMaster.objects.all().values_list('cID', 'cName', 'address', 'email', 'gstIN'):
                writer.writerow(cust)

            response['Content-Disposition'] = 'attachment; filename="customers.csv"'
            return response

    context = {'cust': cust, 'CustAdd': CustAdd}

    return render(request, 'celloApp/customer.html', context)


def edit_customer(request, pk):
    if (chkLogin()==False):
        return HttpResponseRedirect(reverse('login'))

    item = get_object_or_404(CustomerMaster, pk=pk)

    if request.method == 'POST':

        if request.POST.get('logout'):
            loginTable.objects.filter(pk=1).update(userN='', passW='')
            return HttpResponseRedirect(reverse('login'))

        form = CustomerAddForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('customer')
    else:
        form = CustomerAddForm(instance=item)
        return render(request, 'celloApp/edit_Customer.html',
                      {'CustAdd': form})


def order(request):
    if (chkLogin()==False):
        return HttpResponseRedirect(reverse('login'))
    orderForm = OrderForm
    custOrderForm = CustomerForm
    url = request.build_absolute_uri()

    if request.method == 'POST':
        if request.POST.get('addItems'):
            orderTableItems = {}
            form = OrderForm(request.POST)
            if form.is_valid():
                col = form.cleaned_data.get("color")
                len = form.cleaned_data.get("length")
                wid = form.cleaned_data.get("width")
                qua = form.cleaned_data.get("quantity")

            orderTableItems['color'] = col
            orderTableItems['length'] = len
            orderTableItems['width'] = wid
            orderTableItems['quantity'] = qua

            if(tempTableOrder.objects.values_list('pk')):
                for num in tempTableOrder.objects.values_list('pk'):
                    n = num[0]
            else:
                n = 0

            tempTableOrder.objects.create(pk=int(n)+1, order=orderTableItems)

            flag = 1
            messages.success(request, "Added in Order Successful")

        elif request.POST.get('clrItems'):
            tempTableOrder.objects.all().delete()
            flag = 1
            messages.success(request, "Order Basket cleared")

        elif request.POST.get('commitOrder'):
            orderTableItems = {}

            if(tempTableOrder.objects.values_list('pk')):
                for num in tempTableOrder.objects.values_list('pk', 'order'):
                    n1 = num[0]
                    orderTableItems[n1] = ast.literal_eval(num[1])

            form = CustomerForm(request.POST)
            cN = form['cName'].value()
            sta = form['status'].value()
            pay = form['payment'].value()
            dat = form['date'].value()
            param = (eval(cN)[0], sta, pay, dat, orderTableItems)
            if orderTableItems == {}:
                flag = 1
                messages.success(request, "Empty Order")
            else:
                OrderAdd(param)
                logger.warning(
                    ">>>>> CUSTOMER ADD : >>>>> Added {} : {} ".format(
                        eval(cN)[0], orderTableItems))
                messages.success(request, "Committed Order Successful")
            tempTableOrder.objects.all().delete()
            flag = 1
            return HttpResponseRedirect(url)

        elif request.POST.get('logout'):
            loginTable.objects.filter(pk=1).update(userN='', passW='')
            return HttpResponseRedirect(reverse('login'))

    orderTableItemsDisplay = {}
    if(tempTableOrder.objects.values_list('pk')):
        for num in tempTableOrder.objects.values_list('pk', 'order'):
            n1 = num[0]
            orderTableItemsDisplay[n1] = ast.literal_eval(num[1])

    context = {
        'orderForm': orderForm,
        'custOrderForm': custOrderForm,
        'orderTableItemsDisplay' : orderTableItemsDisplay
    }

    return render(request, 'celloApp/order.html', context)


def downloads(request):
    if (chkLogin()==False):
        return HttpResponseRedirect(reverse('login'))

    ClearFiles = ClearFilesForm
    ProcessCSVwhite = ProcessCSVformWhite
    ProcessCSVbrown = ProcessCSVformBrown
    ProcessCSVother = ProcessCSVformOther

    if request.method == 'POST':
        if request.POST.get('entry.csv'):
            file_path = "csvFiles/entry.csv"
            file_name = "entry.csv"
            if (path.exists(file_path)):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="text/csv")
                    # response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                    response[
                        'Content-Disposition'] = 'inline; filename=' + file_name
                    return response
            else:
                flag = 1
                messages.success(request, "File not found")
                return HttpResponseRedirect(reverse('downloads'))

        elif request.POST.get('JumboWhite.csv'):
            file_path = "csvFiles/jumboWhite.csv"
            file_name = "jumboWhite.csv"
            if (path.exists(file_path)):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="text/csv")
                    response[
                        'Content-Disposition'] = 'inline; filename=' + file_name
                    return response
            else:
                flag = 1
                messages.success(request, "File not found")
                return HttpResponseRedirect(reverse('downloads'))

        elif request.POST.get('JumboBrown.csv'):
            file_path = "csvFiles/jumboBrown.csv"
            file_name = "jumboBrown.csv"
            if (path.exists(file_path)):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="text/csv")
                    response[
                        'Content-Disposition'] = 'inline; filename=' + file_name
                    return response
            else:
                flag = 1
                messages.success(request, "File not found")
                return HttpResponseRedirect(reverse('downloads'))

        elif request.POST.get('JumboOther.csv'):
            file_path = "csvFiles/jumboOther.csv"
            file_name = "jumboOther.csv"
            if (path.exists(file_path)):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="text/csv")
                    response[
                        'Content-Disposition'] = 'inline; filename=' + file_name
                    return response
            else:
                flag = 1
                messages.success(request, "File not found")
                return HttpResponseRedirect(reverse('downloads'))

        elif request.POST.get('order.csv'):
            file_path = "csvFiles/order.csv"
            file_name = "order.csv"
            if (path.exists(file_path)):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="text/csv")
                    response[
                        'Content-Disposition'] = 'inline; filename=' + file_name
                    return response
            else:
                flag = 1
                messages.success(request, "File not found")
                return HttpResponseRedirect(reverse('downloads'))

        elif request.POST.get('logFile'):
            file_path = "logs/affix.log"
            file_name = "log.log"
            if (path.exists(file_path)):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="text/csv")
                    response[
                        'Content-Disposition'] = 'inline; filename=' + file_name
                    return response
            else:
                flag = 1
                messages.success(request, "File not found")
                return HttpResponseRedirect(reverse('downloads'))

        elif request.POST.get('process_csv_white'):
            form = ProcessCSVformWhite(request.POST)
            file_path = "csvFiles/ProcessedTapes/White/" + form['white'].value(
            )
            file_name = form['white'].value()
            if (path.exists(file_path)):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="text/csv")
                    response[
                        'Content-Disposition'] = 'inline; filename=' + file_name
                    return response
            else:
                flag = 1
                messages.success(request, "File not found")
                return HttpResponseRedirect(reverse('downloads'))

        elif request.POST.get('process_csv_brown'):
            form = ProcessCSVformBrown(request.POST)
            file_path = "csvFiles/ProcessedTapes/Brown/" + form['brown'].value(
            )
            file_name = form['brown'].value()
            if (path.exists(file_path)):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="text/csv")
                    response[
                        'Content-Disposition'] = 'inline; filename=' + file_name
                    return response
            else:
                flag = 1
                messages.success(request, "File not found")
                return HttpResponseRedirect(reverse('downloads'))

        elif request.POST.get('process_csv_other'):
            form = ProcessCSVformOther(request.POST)
            file_path = "csvFiles/ProcessedTapes/Other/" + form['other'].value(
            )
            file_name = form['other'].value()
            if (path.exists(file_path)):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="text/csv")
                    response[
                        'Content-Disposition'] = 'inline; filename=' + file_name
                    return response
            else:
                flag = 1
                messages.success(request, "File not found")
                return HttpResponseRedirect(reverse('downloads'))

        elif request.POST.get('clrFile'):
            form = ClearFilesForm(request.POST)
            fileName = form['file'].value()
            if fileName == "entry.csv":
                createEntry()
                flag = 1
                messages.success(request, "File Cleared")
            elif fileName == "jumboWhite.csv" or fileName == "jumboBrown.csv" or fileName == "jumboOther.csv":
                createJumboColor(fileName)
                flag = 1
                messages.success(request, "File Cleared")
            elif fileName == "order.csv":
                createOrder()
                flag = 1
                messages.success(request, "File Cleared")

        elif request.POST.get('logout'):
            loginTable.objects.filter(pk=1).update(userN='', passW='')
            return HttpResponseRedirect(reverse('login'))

        elif request.POST.get('reset'):
            resetAll()
            CelloTypes.objects.get_or_create(color='White', quantityInStock=0)
            CelloTypes.objects.get_or_create(color='Brown', quantityInStock=0)
            CelloTypes.objects.get_or_create(color='Other', quantityInStock=0)
            loginTable.objects.get_or_create(pk=1, userN='', passW='')
            usersTable.objects.get_or_create(pk=1, userNames='bas', passwords='bas')

            # CSV Files
            createJumboColor('jumboWhite.csv')
            createJumboColor('jumboBrown.csv')
            createJumboColor('jumboOther.csv')
            createEntry()
            createOrder()

            arr = []
            base = "csvFiles/ProcessedTapes/White"
            for entry in os.listdir(base):
                arr.append(entry)
            for item in arr:
                createProcessed(item,'White')

            arr = []
            base = "csvFiles/ProcessedTapes/Brown"
            for entry in os.listdir(base):
                arr.append(entry)
            for item in arr:
                createProcessed(item,'Brown')

            arr = []
            base = "csvFiles/ProcessedTapes/Other"
            for entry in os.listdir(base):
                arr.append(entry)
            for item in arr:
                createProcessed(item,'Other')

    context = {
        'ClearFiles': ClearFiles,
        'ProcessCSVwhite': ProcessCSVwhite,
        'ProcessCSVbrown': ProcessCSVbrown,
        'ProcessCSVother': ProcessCSVother,
    }

    return render(request, 'celloApp/downloads.html', context)


def rawMaterial(request):
    if (chkLogin()==False):
        return HttpResponseRedirect(reverse('login'))

    RawForm = RawMaterialForm
    raw = CelloTypes.objects.all()

    if request.method == 'POST':
        if request.POST.get('add'):
            form = RawMaterialForm(request.POST)
            col = form['color'].value()
            qua = form['quantityInStock'].value()
            str1 = "Submit button : add, {}, {}".format(col, qua)
            RawEdit('add', col, qua)
            msg = appendJumbo(
                (str(datetime.date.today()), 'Add ' + col, qua, '', col))
            messages.success(request, msg)
            flag = 1
            messages.success(request, "Added Jumbo successfully")
            logger.warning(
                ">>>>> RAW MATERIAL ADD : >>>>> Added {} : {}".format(
                    col, qua))

        elif request.POST.get('sub'):
            form = RawMaterialForm(request.POST)
            col = form['color'].value()
            qua = form['quantityInStock'].value()
            str1 = "Submit button : sub, {}, {}".format(col, qua)
            RawEdit('sub', col, qua)
            msg = appendJumbo(
                (str(datetime.date.today()), 'Sub ' + col, '', qua, col))
            messages.success(request, msg)
            flag = 1
            messages.success(request, "Removed Jumbo successfully")
            logger.warning(
                ">>>>> RAW MATERIAL DEL : >>>>> Deleted {} : {}".format(
                    col, qua))

        elif request.POST.get('logout'):
            loginTable.objects.filter(pk=1).update(userN='', passW='')
            return HttpResponseRedirect(reverse('login'))

    context = {
        'RawForm': RawForm,
        'raw': raw,
    }
    return render(request, 'celloApp/rawMaterial.html', context)


def allOrders(request):
    if (chkLogin()==False):
        return HttpResponseRedirect(reverse('login'))
    order = OrderTable.objects.order_by('oID')
    # process = Processed.objects.order_by('color', 'length')

    if request.method == 'POST':
        if request.POST.get('logout'):
            loginTable.objects.filter(pk=1).update(userN='', passW='')
            return HttpResponseRedirect(reverse('login'))

        elif request.POST.get('dateSelection'):
            fro = userNform = request.POST['fromDate']
            to = userNform = request.POST['toDate']
            if (fro!='' and to!=''):
                order = OrderTable.objects.order_by('oID').filter(date__range=[fro, to])

        elif request.POST.get('exportOrd'):
            response = HttpResponse(content_type='text/csv')

            writer = csv.writer(response)
            writer.writerow(['oID', 'Customer Name', 'Order Details', 'Status', 'Payment', 'Date'])

            order = OrderTable.objects.all().values_list('oID', 'cName', 'orderDetails', 'status', 'payment', 'date')

            fro = userNform = request.POST['fromDate']
            to = userNform = request.POST['toDate']
            if (fro!='' and to!=''):
                order = OrderTable.objects.order_by('oID').filter(date__range=[fro, to]).values_list('oID', 'cName', 'orderDetails', 'status', 'payment', 'date')

            for ord in order:
                writer.writerow(ord)

            response['Content-Disposition'] = 'attachment; filename="orders.csv"'
            return response

    context = {'orderTable': order,}
    return render(request, 'celloApp/allOrders.html', context)
