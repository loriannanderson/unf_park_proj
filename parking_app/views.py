from django.shortcuts import render, redirect

from parking_app.models import Contact,Product,OrderUpdate,Orders,Registration
from django.contrib import messages
from math import ceil
from parking_app import keys
from .forms import RegistrationForm
from django.conf import settings
MERCHANT_KEY=keys.MK
import json
from django.views.decorators.csrf import  csrf_exempt
# from PayTm import Checksum

# Create your views here.
def index(request):

    allProds = []
    catprods=[]
    catprods = Product.objects.values('category','id')
    # print(catprods)
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod= Product.objects.filter(category=cat)
        n=len(prod)
        # this displays 3 items per row...
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params= {'allProds':allProds}
    return render(request,"index.html",params)

    
def contact(request):
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        desc=request.POST.get("desc")
        pnumber=request.POST.get("pnumber")
        myquery=Contact(name=name,email=email,desc=desc,phonenumber=pnumber)
        myquery.save()
        messages.info(request,"Thank you for contacting us, expect a response within 2 business days. ")
        return render(request,"contact.html")


    return render(request,"contact.html")

def about(request):
    return render(request,"about.html")



def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Login & Try Again")
        return redirect('/auth/login')

    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amt')
        # streamline orders - not necessary it's in profile.
        Order = Orders(items_json=items_json,name=name,amount=amount, email="", address1="",address2="",city="",state="",zip_code="",phone="")
        print(amount)
        # TODO - don't save order items JSON - one record per permit... probably need to limit orders only one active at any time... maybe a motorcycle and a car?
        Order.save()
        update = OrderUpdate(order_id=Order.order_id,update_desc="the order has been placed")
        update.save()
        thank = True

# until paypal integrated...
# PAYMENT INTEGRATION

        # id = Order.order_id
        # oid=str(id)+"ShopyCart"
        # param_dict = {
        #
        #     'MID':keys.MID,
        #     'ORDER_ID': oid,
        #     'TXN_AMOUNT': str(amount),
        #     'CUST_ID': email,
        #     'INDUSTRY_TYPE_ID': 'Retail',
        #     'WEBSITE': 'WEBSTAGING',
        #     'CHANNEL_ID': 'WEB',
        #     'CALLBACK_URL': 'http://127.0.0.1:8000/handlerequest/',
        #
        # }
        # # param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        # return render(request, 'paytm.html', {'param_dict': param_dict})

    return render(request, 'checkout.html')


@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    # TODO integrate paypal
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    # verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    # if verify:
    if 1 == 2:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
            a=response_dict['ORDERID']
            b=response_dict['TXNAMOUNT']
            rid=a.replace("ShopyCart","")

            print(rid)
            filter2= Orders.objects.filter(order_id=rid)
            print(filter2)
            print(a,b)
            for post1 in filter2:

                post1.oid=a
                post1.amountpaid=b
                post1.paymentstatus="PAID"
                post1.save()
            print("run agede function")
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'paymentstatus.html', {'response': response_dict})

def createRegistration(request):
    # todo - connect this to something on my profile page.  lost those buttons when combined registration & profile
    # tried crispy forms...
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            reg = form.save(commit=False)
            reg.user = request.user
            reg.save() # create in db
            return redirect('/home')
    else:
        form = RegistrationForm()
    context={'form':form}
    return render(request,'create_registration.html', context)

def updateRegistration(request, ):
    #todo IMPLEMENT -  need to get users profile and populate form if get - or save when post
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            reg = form.save(commit=False)
            reg.user = request.user
            reg.save() # create in db
            return redirect('/home')
        else:
            form = RegistrationForm()
    context={'form':form}
    return render(request,'create_registration.html', context)

def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Login & Try Again")
        return redirect('/auth/login')

    #get user's registration
    registration = Registration.objects.filter(user=request.user).first()
    print(registration)
    currentuser=request.user.username
    permits=Orders.objects.filter(email=currentuser)



    # context ={"items":items,"status":status}
    context = {"registration":registration,"permits":permits}
    # print(currentuser)
    return render(request,"profile.html",context)