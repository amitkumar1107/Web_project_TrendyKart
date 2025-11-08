from django.shortcuts import render, redirect
from django.contrib.auth.models  import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import Product,customer,Cart,Order,OrderItem,profile,orderplaced
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import customeregistrationform,CustomerAddressForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from pymongo import MongoClient
from django.db.models import Q

# Connect to MongoDB
import os
MONGODB_URI = os.getenv('MONGODB_URI')
client = MongoClient(MONGODB_URI)
# Select your database and collection
db = client["fastapilearn"]

collection = db["web_product"]

# Get all documents
documents = collection.find({"category" : "M"})


#home

class productview(View):
    def get(self,request):
        products = Product.objects.all()
        return render(request, 'home.html', {'products': products})
# Register Page
class register_page(View):
    def get(self, request):
        form = customeregistrationform()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = customeregistrationform(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Automatically log in the user after registration
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome {username}! Your account has been created.')
                return redirect('home')  # Redirect to your homepage or dashboard

        # If form is invalid or login fails, show the form again
        return render(request, 'register.html', {'form': form})
def about(request):
    return render(request, 'about.html')


#details page
def product1(request, id):
    product_obj = Product.objects.get(id=id) # Fetch the product by ID
    return render(request, 'prodect1.html', {'prod': product_obj})

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        users = request.user
        
        # Fetch the user's address from the 'customer' model
        address = customer.objects.filter(user=users)
        
        # Fetch the user's orders from the 'orderplaced' model
        orders = orderplaced.objects.filter(user=users).order_by('-order_date')
        
        # Fetch the user's profile picture from the 'customer' model (assuming it exists)
        user_pic = customer.objects.filter(user=users).first()  # Using .first() to safely handle None

        return render(request, 'profile.html', {
            'users': users, 
            'orders': orders,  # Fix variable name (was order)
            'addresses': address,
            'user_pic': user_pic  # Passing the user's profile picture
        })

@method_decorator(login_required, name='dispatch')
class add(View):
    def get(self, request):
        form = CustomerAddressForm()
        return render(request, "address.html", {'form': form})

    def post(self, request):
        form = CustomerAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)  # Don't save yet
            address.user = request.user  # Assign the logged-in user
            address.save()  # Now save to the database
            return redirect('profile')  # Redirect after saving
        return render(request, "address.html", {'form': form})
    


    # Cart Page
@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)  # Fetch user's cart items
    # add = User.objects.filter(user=request.user)  # Fetch user's cart items
    total_price = sum(item.product.price * item.quantity for item in cart_items)  # Calculate total price
    user_addresses = customer.objects.filter(user=request.user)
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        "user_addresses": user_addresses
    }
    return render(request, 'cart.html', context)


@login_required
def add_to_cart(request, product_id):
    """Function to add a product to the cart."""
    
    # Step 1: Fetch the product from the database
    product = get_object_or_404(Product, id=product_id)
    
    # Step 2: Check if the product is already in the cart
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

    # Step 3: If product exists in cart, increase quantity
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    # Step 4: Redirect to the cart page after adding the product
    return redirect('cart')

def remove_from_cart(request, cart_id):
    cart_item = Cart.objects.filter(id=cart_id, user=request.user).first()  # Fetch item

    if not cart_item:
        print(f"Cart item with ID {cart_id} not found for user {request.user}")  # Debugging
        return redirect('cart')  # Redirect if item does not exist

    cart_item.delete()  
    return redirect('cart')


@login_required
def buy_now(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)

    if not cart_items.exists():
        messages.error(request, "Your cart is empty!")
        return redirect('cart')

    # ✅ Fetch the first matching customer (safe fix)
    cust = customer.objects.filter(user=user).first()
    if not cust:
        messages.error(request, "Please complete your profile before ordering!")
        return redirect('profile')

    # ✅ Create the Order
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    order = Order.objects.create(
        user=user,
        product_name=", ".join([item.product.product_name for item in cart_items]),
        quantity=sum([item.quantity for item in cart_items]),
        total_price=total_price
    )

    # ✅ Create entries in OrderItem
    for item in cart_items:
        OrderItem.objects.create(
            product_name=item.product.product_name,
            order=order,
            product=item.product,
            quantity=item.quantity
        )

    # ✅ Create entries in orderplaced
    for item in cart_items:
        orderplaced.objects.create(
            user=user,
            customer=cust,
            product=item.product,
            quantity=item.quantity
        )

    # ✅ Clear the cart after placing order
    cart_items.delete()

    messages.success(request, "Order placed successfully!")
    return render(request, 'order_success.html')



def order_succes(request):
    if request.method == 'POST':
        product_name = request.POST['product_name']
        quantity = int(request.POST['quantity'])
        
        # Fetch the product's price from the Product model (assuming the product exists)
        try:
            product = Product.objects.get(name=product_name)
            total_price = product.price * quantity  # Calculate the total price

            # Create the order and save it
            order = Order(user=request.user, product_name=product_name, quantity=quantity, total_price=total_price)
            order.save()

            return redirect('profile.html')  # Redirect to profile page after saving the order
        except Product.DoesNotExist:
            # Handle the case where the product does not exist
            return render(request, 'order_error.html', {'error': 'Product not found'})
        
    return render(request, 'order_success.html')

def search(request):
    query = request.GET.get('q', '')
    all_products = Product.objects.all()
    products = [
        p for p in all_products
        if query.lower() in p.product_name.lower()
        or query.lower() in p.category.lower()
        or query.lower() in p.dec.lower()
    ]
    return render(request, 'home.html', {"products": products, "query": query})
