from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
import bcrypt

# ----------LOGIN--------------


def index(request):
    return render(request, 'index.html')


# def register(request):
#     errors = User.objects.validate(request.POST)

#     if len(errors) > 0:
#         for key, value in errors.items():
#             messages.error(request, value, extra_tags=key)
#         return render(request, 'login.html')

#     input_password = request.POST["password"]

#     pw_hash = bcrypt.hashpw(input_password.encode(), bcrypt.gensalt()).decode()
#     newUser = User(
#         first_name=request.POST['first_name'],
#         last_name=request.POST['last_name'],
#         pw_hash=pw_hash,
#         email=request.POST['email']
#     )
#     newUser.save()
#     print("This is our user ****************", newUser)
#     request.session['user_id'] = newUser.id
#     return redirect('/success')


# def log_in(request):
#     userList = User.objects.filter(email=request.POST['your_email'])
#     if userList:
#         user = userList[0]
#         if bcrypt.checkpw(request.POST['pw'].encode(), user.pw_hash.encode()):
#             request.session['user_id'] = user.id
#             request.session['name'] = user.first_name
#             return redirect('/success')
#     messages.error(request, "Incorrect login.")
#     return redirect('/')


# def log_out(request):
#     request.session.clear()
#     return redirect('/')


# def success(request):
#     if "user_id" not in request.session:
#         messages.error(request, "Please log in.")
#         return redirect('/')
#     return redirect('/dashboard')


# ----------Customers Info---------------

def about(request):
    return render(request, 'about.html')

def classes(request):
    return render(request, 'classes.html')

def contact(request):
    return render(request, 'contact.html')

def garden(request):
    return render(request, 'garden.html')

def partner(request):
    return render(request, 'partner.html')

def recipe(request):
    return render(request, 'recipe.html')

def rotation(request):
    return render(request, 'rotation.html')

#-----------Product Search---------------

def bulk(request):
    return render(request, 'bulk.html')

def deals(request):
    return render(request, 'deals.html')

def flowers(request):
    return render(request, 'flowers.html')

def produce(request):
    return render(request, 'produce.html')

def specialty(request):
    return render(request, 'specialty.html')

def subscriptions(request):
    return render(request, 'subscriptions.html')

#------------Purchase Info-------------

def productDetails(request):
    return render(request, 'productDetails.html')

def cart(request):
    return render(request, 'cart.html')








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

    return render(request, 'viewProduct.html', context)


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
