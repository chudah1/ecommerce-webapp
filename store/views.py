
from store.forms import CreateUserForm
from django.shortcuts import redirect, render
from store.models import *
from django.contrib import messages


from django.http import JsonResponse
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import authenticate


# Create your views here.
def home(request):
    return render(request, template_name="store/home.html")


def store(request):
    products = Product.objects.all()

    if request.user.is_authenticated:
        # setting up the one to one relationship with user and customer
        customer = request.user.customer
        # find whether the order exists or create
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items


    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
    return render(request, template_name="store/store.html", context={"products": products, "items":items})


def cart(request):
    if request.user.is_authenticated:
        # setting up the one to one relationship with user and customer
        Customer = request.user.customer
        # find whether the order exists or create
        order, created = Order.objects.get_or_create(customer=Customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}

    return render(request, template_name="store/cart.html", context={"items": items, "order": order})


@login_required(login_url="login")
def checkout(request):
    if request.user.is_authenticated:
        # setting up the one to one relationship with user and customer
        Customer = request.user.customer
        # find whether the order exists or create
        order, created = Order.objects.get_or_create(customer=Customer, complete=False)
        items = order.orderitem_set.all()
    else:
        # creating an empty cart for unauthorized users
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
    return render(request, template_name="store/checkout.html",
                  context={"checkout": checkout, "items": items, "order": order})

@authenticate
def register(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():

            form.save()
                #automatically login the user 
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password1=password)

        
            login(request, user)
            messages.success(request, f"Account Created successfully for {{user}}")
            return redirect("store")
        else:
            return redirect("register")
    else:
        form=CreateUserForm()
    return render(request, template_name="store/register.html", context={"form":form})

@authenticate
def loginPage(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
            # checking the database using the authenticate function to see whether username and name password exists and return a user object
        user = authenticate(request, username=username, password=password)

            # login the user and redirect to the store
        if user is not None:
            login(request, user)
            return redirect("store")
        else:
            messages.warning(request, "Username and password does not match! ")
    return render(request, template_name="store/login.html")


def logoutPage(request):
    logout(request)
    messages.info(request, "logged out successfully!")
    return redirect("login")




def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    return JsonResponse("Payment complete", safe=False)
