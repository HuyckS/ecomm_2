from django.http.response import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
import bcrypt
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY
google_api_key = settings.GOOGLE_API_KEY

#--------Helper Functions------

def checkCustomer(request):
    if "user_id" not in request.session:
        customer_id = 0
        customer_name = 'customer'
    else:
        customer_id = request.session["user_id"]
        customer_logged = User.objects.get(id=customer_id)
        customer_name = customer_logged.first_name
    cart_items = CartItem.objects.filter(user_id=customer_id)
    total = 0;
    for item in cart_items:
            if item.user_id == customer_id:
                total = total + item.total
    context = {
        'customer_id' : customer_id,
        'customer': customer_name,
        'cart_items': cart_items,
        'total': total,
    }
    return context

# ----------LOGIN--------------


def index(request):
    context = checkCustomer(request)
    context.update(key=google_api_key)
    return render(request, 'index.html', context)

def signIn(request):
    return render(request, 'login.html')
    
def register(request):
    errors = User.objects.validate(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return render(request, 'login.html')

    input_password = request.POST["password"]

    pw_hash = bcrypt.hashpw(input_password.encode(), bcrypt.gensalt()).decode()
    newUser = User(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        username=request.POST['username'],
        pw_hash=pw_hash,
        email=request.POST['email']
    )
    newUser.save()
    print("This is our user ****************", newUser)
    request.session['user_id'] = newUser.id
    return redirect('/success')


def log_in(request):
    userList = User.objects.filter(email=request.POST['your_email'])
    if userList:
        user = userList[0]
        if bcrypt.checkpw(request.POST['pw'].encode(), user.pw_hash.encode()):
            request.session['user_id'] = user.id
            request.session['name'] = user.first_name
            return redirect('/success')
    messages.error(request, "Incorrect login.")
    return redirect('/login')


def log_out(request):
    request.session.clear()
    return redirect('/')


def success(request):
    if "user_id" not in request.session:
        messages.error(request, "Please log in.")
        return redirect('/login')
    return redirect('/')


# ----------Site Info---------------

def about(request):
    context = checkCustomer(request)
    return render(request, 'about.html', context)

def classes(request):
    context = checkCustomer(request)
    return render(request, 'classes.html', context)

def contact(request):
    context = checkCustomer(request)
    return render(request, 'contact.html', context)

def garden(request):
    context = checkCustomer(request)
    return render(request, 'garden.html', context)

def partner(request):
    context = checkCustomer(request)
    return render(request, 'partner.html', context)

def recipe(request):
    context = checkCustomer(request)
    return render(request, 'recipe.html', context)

def rotation(request):
    context = checkCustomer(request)
    return render(request, 'rotation.html', context)

#-----------Product Search---------------

def bulk(request):
    customer = checkCustomer(request)

    products = Product.objects.all()
    bulk_list = Product.objects.filter(category="bulk")

    context = {
        'user': customer,
        'all_products': bulk_list,
    }

    return render(request, 'bulk.html', context)

def deals(request):
    customer = checkCustomer(request)

    products = Product.objects.all()
    deals_list = Product.objects.filter(category="deals")

    context = {
        'user': customer,
        'all_products': deals_list,
    }

    return render(request, 'deals.html', context)

def flowers(request):
    customer = checkCustomer(request)

    products = Product.objects.all()
    flowers_list = Product.objects.filter(category="flowers")

    context = {
        'user': customer,
        'all_products': flowers_list,
    }

    return render(request, 'flowers.html', context)

def produce(request):
    customer = checkCustomer(request)

    products = Product.objects.all()
    produce_list = Product.objects.filter(category="produce")

    context = {
        'user': customer,
        'all_products': produce_list,
    }

    return render(request, 'produce.html', context)

def specialty(request):
    customer = checkCustomer(request)

    products = Product.objects.all()
    specialty_list = Product.objects.filter(category="specialty")

    context = {
        'user': customer,
        'all_products': specialty_list,
    }

    return render(request, 'specialty.html', context)

def subscription(request):
    customer = checkCustomer(request)

    products = Product.objects.all()
    subscriptions_list = Product.objects.filter(category="subscription")

    context = {
        'user': customer,
        'all_products': subscriptions_list,
    }

    return render(request, 'subscriptions.html', context)

def productDetails(request):
    context = checkCustomer(request)
    print(context)
    context.update({
        "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
    })

    return render(request, 'productDetails.html', context)

#------------Purchase Info-------------

def cart(request):
    context = checkCustomer(request)
    return render(request, 'cart.html', context)

def checkout(request):
    context = checkCustomer(request)
    return render(request, 'checkout.html', context)

def paymentFailure(request):
    context = checkCustomer(request)
    return render(request, 'paymentFailure.html', context)

def paymentSuccess(request):
    context = checkCustomer(request)
    return render(request, 'paymentSuccess.html', context)

def orderHistory(request):
    context = checkCustomer(request)
    return render(request, 'orderHistory.html', context)

def add_to_cart(request):
    context = checkCustomer(request)

    add_user_id = request.session['user_id']
    add_item = request.POST['itemToAdd']
    add_quantity = float(request.POST['quantity'])
    add_price = float(request.POST['price']) * add_quantity

    newCartItem = CartItem.objects.create(
        user_id=add_user_id,
        product=add_item,
        quantity=add_quantity,
        total=add_price,
    )

    newCartItem.save()

    return redirect('/cart')

def removeFromCart(request, item_id):

    deleted_product = CartItem.objects.get(id=item_id).delete()

    return redirect('/cart')


def create_checkout_session(request):
        user = int(request.POST['user_id'])
        items = CartItem.objects.filter(user_id=user)
        amount = 0
        for item in items:
            amount = amount + int(item.quantity)

        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': 'price_1JZjPIIDb1tCitGQhKLhO1s4',
                    'quantity': amount,
                },
            ],
            payment_method_types=[
                'card',
            ],
            mode='payment',
            success_url= 'http://localhost:8000/payment/success',
            cancel_url='http://localhost:8000/payment/failure',
        )
        return redirect(checkout_session.url, code=303)

# ------------Products------------------


def dashboard(request):
    if "user_id" not in request.session:
        messages.error(request, "Please log in.")
        return redirect('/')

    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    products = Product.objects.all()

    context = {
        'all_products': products,
        'user': user,
        'all_created_products': user.created_products.all(),
    }
    return render(request, 'dashboard.html', context)


def newProductForm(request):
    if "user_id" not in request.session:
        messages.error(request, "Please log in.")
        return redirect('/')
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    context = {'user': user}
    return render(request, 'newProduct.html', context)


def createProduct(request):
    if "user_id" not in request.session:
        messages.error(request, "Please log in.")
        return redirect('/')

    errors = Product.objects.validate_product(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
            return redirect('/products/new')

    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    add_title = request.POST['title']
    add_desc = request.POST['desc']
    add_category = request.POST['category']

    newProduct = Product.objects.create(
        title=add_title,
        desc=add_desc,
        category=add_category,
        # ADD OTHER FIELDS AND UPDATE MODEL
        product_creator=user
    )

    newProduct.save()

    return redirect('/dashboard')


def showProduct(request, product_id):
    customer = checkCustomer(request)

    product = Product.objects.filter(id=product_id)

    context = {
        'user': customer,
        'this_product': product[0],
    }

    return render(request, 'productDetails.html', context)


def editProduct(request, product_id):
    if "user_id" not in request.session:
        messages.error(request, "Please log in.")
        return redirect('/')

    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    product = Product.objects.filter(id=product_id)

    context = {
        'user': user,
        'this_product': product[0]
    }

    return render(request, 'editProduct.html', context)


def updateProduct(request, product_id):
    if "user_id" not in request.session:
        messages.error(request, "Please log in.")
        return redirect('/')

    errors = Product.objects.validate_product(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
            return redirect(f"/products/edit/{product_id}")

    updatedProduct = Product.objects.get(id=product_id)
    updatedProduct.title = request.POST['title']
    updatedProduct.desc = request.POST['desc']
    updatedProduct.location = request.POST['loc']

    updatedProduct.save()

    return redirect('/dashboard')


def removeProduct(request, product_id):
    if "user_id" not in request.session:
        messages.error(request, "Please log in.")
        return redirect('/')
    deleted_product = Product.objects.get(id=product_id).delete()

    return redirect('/dashboard')
