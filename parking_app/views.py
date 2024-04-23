from django.shortcuts import render, redirect

from parking_app.models import Contact,Product,OrderUpdate,Orders,Registration
from django.contrib import messages
from math import ceil
from parking_app import keys
from .forms import RegistrationForm
from django.conf import settings
from django.http import FileResponse, Http404
MERCHANT_KEY=keys.MK
import json
from django.views.decorators.csrf import  csrf_exempt
# from PayTm import Checksum
from paypal.standard.forms import PayPalPaymentsForm
import uuid
from django.urls import reverse


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
def parking_map(request):
    try:
        return FileResponse(open("static/images/parking_map.pdf", 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404('not found')

def about(request):
    return render(request,"about.html")


def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Login & Try Again")
        return redirect('/auth/login')
    user_profile = Registration.objects.get(user=request.user)
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amt')
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2','')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        # save each permit as  separate order - so it can be displayed in profile - not as json
        orders = json.loads(items_json)
        permits = orders.keys() # need to know what items were ordered.
        print(permits)
        for permit in permits:
            print (orders[permit])
            product_id = int(permit.replace("pr",""))
            print (product_id)
            # add user to each order so they can be tracked back for my profile display

            product = Product.objects.get(id=product_id)
            permit_order = Orders(user=request.user, product=product, name=name, amount=product.price, email=email, address1=address1,
                                   address2=address2, city=city, state=state, zip_code=zip_code, phone=phone)
            permit_order.save()

            # not sure how to handle updates  until Paypal done... so keep the code for now.
            update = OrderUpdate(order_id=permit_order.order_id,update_desc="the order has been placed")
            update.save()

        thank = True
        product = Product.objects.get(id=product_id)

        host = request.get_host()

        paypal_checkout = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': amount,
            'item_name': items_json,
            'invoice': uuid.uuid4(),
            'currency_code': 'USD',
            'notify_url': f"http://{host}{reverse('paypal-ipn')}",
            'return_url': f"http://{host}{reverse('payment-success', kwargs={'product_id': product.id})}",
            'cancel_url': f"http://{host}{reverse('payment-failed', kwargs={'product_id': product.id})}",
        }

        paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

        context = {
            'amount':amount,
            'product': items_json,
            'paypal': paypal_payment
        }

        return render(request, 'paypalCheckout.html', context=context)


    context={'profile':user_profile,
             }
    return render(request, 'checkout.html', context=context)

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
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        print ("create registration" )

        if form.is_valid(): #TODO -
            print("in createRegistration POST form valid")
            if request.method == "POST":
                myprofile = Registration(
                user = request.user,
                first_name = request.POST.get("first_name"),
                last_name = request.POST.get("last_name"),
                student_id_num = request.POST.get("student_id_num"),
                employee_id_num = request.POST.get('employee_id_num'),
                address_1 = request.POST.get('address_1'),
                address_2 = request.POST.get('address_2'),
                city = request.POST.get('city'),
                state = request.POST.get('state'),
                zip_code = request.POST.get('zip_code'),
                phone = request.POST.get('phone'),
                vehicle_make = request.POST.get('vehicle_make'),
                vehicle_model = request.POST.get('vehicle_model'),
                color = request.POST.get("color"),
                license_plate = request.POST.get('license_plate'),
                vehicle2_make = request.POST.get('vehicle2_make'),
                vehicle2_model = request.POST.get('vehicle2_model'),
                color2 = request.POST.get('color2'),
                license2_plate = request.POST.get('license2_plate'),
                )
                myprofile.save()
                currentuser = request.user.username
                permits = Orders.objects.filter(email=currentuser)
                context = {"registration": myprofile, "permits": permits}
                return render(request, "profile.html", context)
            # return render(request, "profile.html", context)

    else:
        form = RegistrationForm()
    context={'form':form}
    return render(request,'create_registration.html', context)

def updateRegistration(request):
    # get users profile
    user_reg = Registration.objects.get(user=request.user)

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        print ("update registration" )

        if form.is_valid(): #TODO -
            print("in createRegistration POST form valid")
            if request.method == "POST":
                user_reg.first_name = request.POST.get("first_name")
                user_reg.last_name = request.POST.get("last_name")
                user_reg.student_id_num = request.POST.get("student_id_num")
                user_reg.employee_id_num = request.POST.get('employee_id_num')
                user_reg.address_1 = request.POST.get('address_1')
                user_reg.address_2 = request.POST.get('address_2')
                user_reg.city = request.POST.get('city')
                user_reg.state = request.POST.get('state')
                user_reg.zip_code = request.POST.get('zip_code')
                user_reg.phone = request.POST.get('phone')
                user_reg.vehicle_make = request.POST.get('vehicle_make')
                user_reg.vehicle_model = request.POST.get('vehicle_model')
                user_reg.color = request.POST.get("color")
                user_reg.license_plate = request.POST.get('license_plate')
                user_reg.vehicle2_make = request.POST.get('vehicle2_make')
                user_reg.vehicle2_model = request.POST.get('vehicle2_model')
                user_reg.color2 = request.POST.get('color2')
                user_reg.license2_plate = request.POST.get('license2_plate')

                user_reg.save()

                currentuser = request.user.username
                permits = Orders.objects.filter(email=currentuser)
                context = {"registration": user_reg, "permits": permits}
                return render(request, "profile.html", context)
            # return render(request,"profile.html",context)

    context={'form':user_reg}
    return render(request,'update_registration.html', context)

def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Login & Try Again")
        return redirect('/auth/login')

    #get user's registration
    registration = Registration.objects.filter(user=request.user).first()
    print(registration)
    currentuser=request.user.username
    permits=Orders.objects.filter(user=request.user)

    context = {"registration":registration,"permits":permits}
    return render(request,"profile.html",context)

def paypalcheckout(request, paydata):

    # product = Product.objects.get(id=product_id)

    host = request.get_host()

    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': product.price,
        'item_name': product.name,
        'invoice': uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('payment-success', kwargs = {'product_id': product.id})}",
        'cancel_url': f"http://{host}{reverse('payment-failed', kwargs = {'product_id': product.id})}",
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    context = {
        'product': product,
        'paypal': paypal_payment
    }

    return render(request, 'checkout.html', context)
#
def PaymentSuccessful(request, product_id):

    product = Product.objects.get(id=product_id)

    return render(request, 'payment-success.html', {'product': product})

def paymentFailed(request, product_id):

    product = Product.objects.get(id=product_id)

    return render(request, 'payment-failed.html', {'product': product})