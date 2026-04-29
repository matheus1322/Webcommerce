from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, login, logout
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib import messages
from webecommerce.models import Product, Order, OrderItem, Category, DiscountCode

#Storefront: Handles Search, Category Filtering, and Cart Badge
def product_list(request):
    category_slug = request.GET.get('category')
    search_query = request.GET.get('search')
    
    categories = Category.objects.all()
    products = Product.objects.all()

    #Filtering Logic
    if category_slug:
        products = products.filter(category__slug=category_slug)
        
    if search_query:
        products = products.filter(name__icontains=search_query) | products.filter(description__icontains=search_query)

    #Cart Badge Logic
    cart_count = 0
    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user, complete=False).first()
        if order:
            cart_count = order.orderitem_set.count()

    context = {
        'products': products,
        'categories': categories,
        'cart_count': cart_count,
    }
    return render(request, 'store/product_list.html', context)

#Authentication: Register and Logout
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! Welcome to the store.")
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('product_list')

#Cart Management: Add, Remove, and Apply Discount
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order, created = Order.objects.get_or_create(user=request.user, complete=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    order_item.quantity += 1
    order_item.save()
    messages.success(request, f"{product.name} added to cart.")
    return redirect('product_list')

@login_required
def remove_from_cart(request, item_id):
    order_item = get_object_or_404(OrderItem, id=item_id, order__user=request.user, order__complete=False)
    product_name = order_item.product.name
    
    if order_item.quantity > 1:
        order_item.quantity -= 1
        order_item.save()
        messages.info(request, f"Reduced quantity of {product_name}.")
    else:
        order_item.delete()
        messages.warning(request, f"Removed {product_name} from your cart.")
    return redirect('cart')

def apply_discount(request):
    if request.method == 'POST':
        code_text = request.POST.get('discount_code')
        try:
            discount = DiscountCode.objects.get(code__iexact=code_text, active=True)
            request.session['discount_id'] = discount.id
            messages.success(request, f"Code applied! You got {discount.discount_percent}% off.")
        except DiscountCode.DoesNotExist:
            request.session['discount_id'] = None
            messages.error(request, "Invalid or expired discount code.")
    return redirect('cart')

def home(request):
    categories = Category.objects.all()
    # We only show the newest 4 products on the home page
    products = Product.objects.all().order_by('-id')[:4]
    return render(request, 'store/home.html', {
        'categories': categories,
        'products': products
    })

#Shopping Cart and Totals
@login_required
def cart(request):
    order = Order.objects.filter(user=request.user, complete=False).first()
    total = 0
    discount_amount = 0
    final_total = 0

    if order:
        total = sum(item.product.price * item.quantity for item in order.orderitem_set.all())
        discount_id = request.session.get('discount_id')
        if discount_id:
            try:
                discount = DiscountCode.objects.get(id=discount_id)
                discount_amount = (total * discount.discount_percent) / 100
            except DiscountCode.DoesNotExist:
                request.session['discount_id'] = None
        
        final_total = total - discount_amount

    context = {
        'order': order,
        'total': total,
        'discount_amount': discount_amount,
        'final_total': final_total
    }
    return render(request, 'store/cart.html', context)

#Checkout: Address and Stock Management
@login_required
def checkout(request):
    order = Order.objects.filter(user=request.user, complete=False).first()
    
    if not order or order.orderitem_set.count() == 0:
        return redirect('product_list')

    if request.method == 'POST':
        order.shipping_address = request.POST.get('address')
        order.complete = True
        order.save()
        
        for item in order.orderitem_set.all():
            product = item.product
            product.stock -= item.quantity
            product.save()
            
        # Clear discount from session after purchase
        if 'discount_id' in request.session:
            del request.session['discount_id']
            
        return render(request, 'store/order_success.html')

    return render(request, 'store/checkout.html', {'order': order})

def about(request):
    return render(request, 'store/about.html')

#Client Area: Profile Update & Order History
@login_required
def profile(request):
    past_orders = Order.objects.filter(user=request.user, complete=True).order_by('-date_ordered')
    
    if request.method == 'POST':
        if 'update_info' in request.POST:
            request.user.first_name = request.POST.get('first_name')
            request.user.last_name = request.POST.get('last_name')
            request.user.email = request.POST.get('email')
            request.user.save()
            messages.success(request, "Profile updated successfully!")
            
        elif 'change_password' in request.POST:
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password updated successfully!")
            else:
                messages.error(request, "Please correct the error below.")
        return redirect('profile')

    return render(request, 'store/profile.html', {'past_orders': past_orders})