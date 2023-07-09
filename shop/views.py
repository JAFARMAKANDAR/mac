from django.shortcuts import render
from .models import Product, Contact, Orders, Orderupdate
from math import ceil
import json

# Create your views here.
from django.http import HttpResponse


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


def search(request):
    return render(request, 'shop/search.html')


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
        return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
    return render(request, 'shop/checkout.html')
