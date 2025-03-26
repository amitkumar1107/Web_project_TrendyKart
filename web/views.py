from django.shortcuts import render, redirect
from django.contrib.auth.models  import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Product,customer,Cart,Order,OrderItem,profile,orderplaced
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import customeregistrationform,CustomerAddressForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages

#home
class productview(View):
    def get(self,request):
        products = Product.objects.all()
        return render(request, 'home.html', {'products': products})
# Register Page
class register_page(View):
    def get (self,request):
        form=customeregistrationform()
        return render(request, 'register.html',{'form':form})
    def post(self,request):
        form=customeregistrationform(request.POST)
        if form.is_valid():
            form.save()
        return render(request, 'register.html',{'form':form})  


def about(request):
    return render(request, 'about.html')


#details page
def product1(request, id):
    product_obj = Product.objects.get(id=id) # Fetch the product by ID
    return render(request, 'prodect1.html', {'prod': product_obj})

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        users = request.user 
        address=customer.objects.filter(user=users)
        order = Product.objects.filter(user=users) if hasattr(Product, 'user') else None
        user_pic=customer.objects.filter(user=users)
        return render(request, 'profile.html', {
            'users': users, 
            'orders': order,  # Fix variable name (was order)
            'addresses': address,
            'user_pic':user_pic  # Now correctly passing addresses
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

    cart_item.delete()  # Delete item if found
    return redirect('cart')


def buy_now(request, id):
    product_obj = Product.objects.get(id=id)
    
    if not request.user.is_authenticated:
        messages.error(request, "Please log in to place an order!")
        return redirect('login')

    # Get Customer Profile
    try:
        customer = customer.objects.get(user=request.user)
    except customer.DoesNotExist:
        messages.error(request, "Please complete your profile before ordering!")
        return redirect('profile')

    # ✅ Create and Save Order
    order =orderplaced.objects.create(
        user=request.user,
        customer=customer,
        product=product_obj,
        quantity=1
    )

    messages.success(request, "Order placed successfully!")
    return redirect('order_success')  # Redirect to order success page
def order_success(request):
    return render(request, 'order_success.html')

class profile_update(View):
    def get(self,request):
        if request =='POST':
            user_name=User.objects.filter


# class orderpleasd(View):
#     def get(request ,id):
#         product_obj = Product.objects.get(id=id)
#         user=request.user
#         orderr=orderpleasd(request.POST)
#         if orderr.is_valid():
#             orderr.save()
        
