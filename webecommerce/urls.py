from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from webecommerce import views

urlpatterns = [
    # Admin Interface
    path('admin/', admin.site.urls),

    # Main Pages
    path('', views.home, name='home'),
    path('shop/', views.product_list, name='product_list'),
    path('about/', views.about, name='about'),

    # Cart & Checkout
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('apply-discount/', views.apply_discount, name='apply_discount'),
    path('checkout/', views.checkout, name='checkout'),

    # User Accounts
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
    path('logout/', views.user_logout, name='logout'),

]

# This allows Django to serve images (shirts/sweatshirts) during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)