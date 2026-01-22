from decimal import Decimal
from django.shortcuts import render,redirect
from .models import Product,Order
from django.http import HttpResponse
import uuid
from django_esewa import EsewaPayment


# Create your views here.
def index(req):
    context = {
        'products': Product.objects.all()
    }

    return render(req, 'index.html', context)

def detail(req, slug):
    context = {
        'product': Product.objects.get(slug=slug)
    }
    return render(req, 'detail.html', context)

def order(req, slug):
    product = Product.objects.get(slug=slug)
    if req.method == "GET":
        return HttpResponse("Invalid access method.", status = 405)
    
    buyer_name = req.POST.get('fullname')
    buyer_phone = req.POST.get('phone')
    quantity = int(req.POST.get('quantity', 1))
    price = Decimal(product.price) * Decimal(quantity)
    tax = price * Decimal('0.13')
    service_charge = price * Decimal('0.05')
    delivery_charge = Decimal('50.00')
    total = price + tax + service_charge + delivery_charge
    uid = uuid.uuid4().hex.upper()
    order = Order.objects.create(
        product = product,
        price = price,
        uid = uid,
        tax = tax,
        total = total,
        service_charge = service_charge,
        delivery_charge = delivery_charge,
        quantity = quantity,
        buyer_name = buyer_name,
        buyer_phone = buyer_phone,

    )
    payment = EsewaPayment(
        product_code="EPAYTEST",
        success_url=f"http://localhost:8000/success/{order.uid}",
        failure_url=f"http://localhost:8000/failure/{order.uid}",
        amount=order.price,
        tax_amount=order.tax,
        total_amount=order.total,
        product_delivery_charge=order.delivery_charge,
        product_service_charge=order.service_charge,
        transaction_uuid=order.uid,
        secret_key="8gBm/:&EnhH.1/q",
    )
    signature = payment.create_signature() #Saves the signature as well as return it

    
    context = {
        'product': product,
        'order': order,
        'form':payment.generate_form()
    }
    return render(req, 'order.html', context)


def success(req, uid):
    order = Order.objects.get(uid=uid)
    payment = EsewaPayment(
        product_code="EPAYTEST",
        success_url=f"http://localhost:8000/success/{order.uid}",
        failure_url=f"http://localhost:8000/failure/{order.uid}",
        amount=order.price,
        tax_amount=order.tax,
        total_amount=order.total,
        product_delivery_charge=order.delivery_charge,
        product_service_charge=order.service_charge,
        transaction_uuid=order.uid,
        secret_key="8gBm/:&EnhH.1/q",
        )
    
    signature = payment.create_signature() #Saves the signature as well as return it

    if payment.is_completed(dev=True):
        order.complete_order()
        return render(req, 'success.html', {'order': order})

    else:
        return redirect('failure', uid=uid) 
    
    

def failure(req, uid):
    order = Order.objects.get(uid=uid)
    order.cancel_order()
    return render(req, 'failure.html', {'order': order})

