import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
import datetime
from .models import *
from user.models import *
from django.contrib.auth.decorators import login_required
from decouple import config



# Create your views here.
########################################## home page views
def homePage(request):
    return render(request, 'store/index.html')


########################################## products page views
@login_required(login_url='login')
def productsPage(request):
    if request.user.is_authenticated:
        customer = request.user.profile
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/products.html', context)


######################################### updateItems views
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.profile
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity +1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity -1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

########################################## carts page views
@login_required(login_url='login')
def cartPage(request):
    if request.user.is_authenticated:
        customer = request.user.profile
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

        if request.method == 'POST':
            # Check if the remove button was clicked
            if 'delete' in request.POST:
                product_id = request.POST.get('delete')

                try:
                    item_to_delete = order.orderitem_set.get(id=product_id)
                    item_to_delete.delete()
                    # Redirect to the cart page after deletion
                    return redirect('cart')
                except OrderItem.DoesNotExist:
                    pass
                
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


######################################### updateItems views
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.profile
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['shipping']['total'])
        order.transaction_id = transaction_id

        if total == float(order.get_cart_total):
            order.complete = True
        order.save()

        ShippingAddress.objects.create( 
            customer=customer, 
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            zipcode=data['shipping']['zipcode']
        )
    return JsonResponse('payment complete', safe=False)


########################################## carts page views
@login_required(login_url='login')
def checkoutPage(request):
    if request.user.is_authenticated:
        customer = request.user.profile
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

        # Convert the price from USD to GHS using the exchange rate
        usd_price = order.get_cart_total
        exchange_rate = 12  # Replace with the actual exchange rate
        ghs_price = (usd_price * exchange_rate) * 100

        customer_mail = customer.email
        
        paystack_public_key = config('PAYSTACK_PUBLIC_KEY')

    context = {'items': items, 'order': order, 
               'cartItems': cartItems, 'customer_mail': customer_mail, 
               'paystack_public_key': paystack_public_key,
               'ghs_price': ghs_price}  # Include the GHS price in the context
    return render(request, 'store/checkout.html', context)





