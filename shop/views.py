from django.shortcuts import render
from .models import Product, Contact, Orders, Orderupdate
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
#from payTm import checksum
# Create your views here.
from django.http import HttpResponse
MERCHANT_KEY = '';

def index(request):
    #products = Product.objects.all()

    allProds =[]
    catprods = Product.objects.values('category',  'id')
    cats =  {item['category'] for item in  catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n//4 + ceil((n/4) - (n//4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params={'allProds': allProds }
    return render(request, "shop/index.html", params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    if request.method == "post":
        name = request.POST.get('name', '')
        email = request.POST.get('print', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')

        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
    return render(request, "shop/contact.html", {'Contact': Contact})


def tracker(request):
    if request.method == "post":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.object.filter(order_id=orderId, email=email)
            if len(order) > 0:
                update = Orderupdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append: ({'text:item.update_desc', 'time:item.timestamp'})
                    response = json.dumps(updates, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse({})
        except Exception as e:
            return HttpResponse({})

    return render(request, "shop/tracker.html")

def searchMatch(query, item):
    ''' return true only if query matches the item'''
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False
def search(request):

    allProds =[]
    query = request.GET.get('search')
    catprods = Product.objects.values('category',  'id')
    cats =  {item['category'] for item in  catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n//4 + ceil((n/4) - (n//4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params={'allProds': allProds}
    if len(allProds) == 0 or len(query) < 4:
        params = {'msg' "pleasee make sure to enter relevent search query"}
    return render(request, "shop/search.html", params)



def Productview(request, myid):
    # fetch the product using the id
    product = Product.objects.filter(id=myid)
    print(product)
    return render(request, 'shop/Prodview.html', {'product': product[0]})


def checkout(request):
    if request.method == "post":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + "" + request.POST.get('address line 2', '')
        state = request.POST.get('state', '')
        city = request.POST.get('city', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, phone=phone, address=address,
                       state=state, zip_code=zip_code, city=city, amount=amount)
        order.save()
        update = Orderupdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        #return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
        #request paytm to transfer the amount to your account after payment by user
        param_dict = {

            'MID': '',
            'ORDER_ID': 'order.order_id',
            'TXN_AMOUNT': '1',
            'CUST_ID': 'email',
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            # 'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',
        }
      #  param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'shop/paytm.html', {'param_dict': param_dict})
    return render(request, 'shop/checkout.html')
@csrf_exempt
def handlerequest(request):
    #paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        checksum = form[i]

    verify = checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})