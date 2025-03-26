from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views
from .forms import loginform
from .views import cart_view,add_to_cart,remove_from_cart,buy_now,order_success

from .views import cart_view,product1,about
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.productview.as_view(),name='home'),
    path('register/', views.register_page.as_view(), name="register"),
    path( "cart/",cart_view,name="cart"),
    path("about/",about,name="about"),
   path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html', authentication_form=loginform), name='login'),
   path('product/<int:id>/',product1,name="product"),
   path('profile/',views.ProfileView.as_view(),name='profile'),
   path('add/',views.add.as_view(),name='add'),
   path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
   path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
   path('cart/remove/<int:cart_id>/', remove_from_cart, name='remove_from_cart'),
   path('cart/buy/<int:id>/', buy_now, name='buy_now'),
   path('order-success/', views.order_success, name='order_success'),
   path('buynow/',views.order_success,name="buynow")

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)