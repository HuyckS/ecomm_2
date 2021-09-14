from django.db import models
import re

# Create your models here.

class UserManager(models.Manager):
    def validate(self, post_data):
        errors = {}
        if len(post_data['first_name']) == 0:
            errors['first_name'] = "First Name required"
        if not re.search('[a-zA-Z]{2,}', post_data['first_name']):
            errors['first_name'] = "Must be greater than 2 characters. Valid Characters include (A-Z) (a-z) (' space -)"
        if len(post_data['last_name']) == 0:
            errors['last_name'] = "Last Name required"
        if not re.search('[a-zA-Z]{2,}', post_data['last_name']):
            errors['last_name'] = "Must be greater than 2 characters. Valid Characters include (A-Z) (a-z) (' space -)"
        if len(post_data['username']) == 0:
            errors['username'] = "Username required"
        if not re.search('[a-zA-Z]{2,}', post_data['username']):
            errors['username'] = "Must be greater than 8 characters. Valid Characters include (A-Z) (a-z) (' space -)"
        if len(post_data['username']) < 8:
            errors['username'] = "Username must be at least 8 characters long."
        if len(post_data['email']) < 7:
            errors['email'] = "Please enter a valid email."
        if not re.search('^[a-z0-9]+[@]\w+[.]\w{2,3}$', post_data['email']):
            errors['email'] = "Please enter a valid email. Valid Characters include: a-z, 0-9, _ @ . "
        if len(post_data['password']) < 8:
            errors['password'] = "Must be at least 8 characters long."
        if post_data['password'] != post_data['confirm_pass']:
            errors['password_not_confirmed'] = "Passwords do not match -- please try again"

        all_users = User.objects.all()

        for user in all_users:
            if user.email == post_data['email']:
                errors['email_taken'] = "That email is already in use, please choose a different email or login."

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    pw_hash = models.CharField(max_length=255)
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # orders

class Admin(User):
    admin_access = models.BooleanField(default=True)
    # products

class Developer(Admin):
    dev_access = models.BooleanField(default=True)

class OrderManager(models.Manager):
    def validate_order(self, post_data):
        errors = {}
        # till need to add validations
        return errors

class Order(models.Model):
    order_date = models.DateField(auto_now=False, auto_now_add=False)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    purchaser = models.ForeignKey(
        User, related_name="orders", on_delete=models.CASCADE)
    objects = OrderManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ProductManager(models.Manager):
    def validate_job(self, post_data):
        errors = {}
        name = post_data['name']
        desc = post_data['desc']
        category = post_data['category']
        if not name or name.isspace():
            errors['name'] = "Must enter a valid name. (Spaces are not a valid name)"
        if not desc or desc.isspace():
            errors['description'] = 'Must enter a valid description. (Spaces are not a valid description)'
        if not category or category.isspace():
            errors['category'] = 'Must enter a valid category. (Spaces are not a valid category)'

        if len(name) < 3 or len(desc) < 3 or len(category) < 3:
            errors['all_fields'] = "All fields must be greater than 3 characters."

        all_products = Product.objects.all()

        for product in all_products:
            if product.name == name and product.desc == desc and product.category == category:
                errors['product_exists'] = "That product already exists. Please update current description or contact product creator for changes."

        return errors

class Product(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField(max_length=255)
    category = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products', blank=True)
    inventory_count = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    product_creator = models.ForeignKey(
        Admin, related_name="created_products", on_delete=models.CASCADE)
    objects = ProductManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CartItemManager(models.Manager):
    def validate_order(self, post_data):
        errors = {}
        # till need to add validations
        return errors

class CartItem(models.Model):
    user_id = models.PositiveIntegerField()
    product = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=9, decimal_places=2)
    total = models.DecimalField(max_digits=9, decimal_places=2)
    objects = CartItemManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)