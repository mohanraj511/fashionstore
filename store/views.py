from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product, Profile, CartItem
from .models import Order,OrderItem
from django.http import JsonResponse 
from django.views.decorators.csrf import csrf_exempt

# ----------------- PRODUCT VIEWS -----------------

def product_list(request):
    products = Product.objects.all()
    categories = products.values_list('category', flat=True).distinct()
    categorized_products = {
        category: products.filter(category=category) for category in categories
    }
    return render(request, 'store/product_list.html', {
        'categorized_products': categorized_products
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/product_detail.html', {'product': product})


# ----------------- CART VIEWS -----------------

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')

@login_required
def checkout_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')

        if payment_method == 'cod':
            # Process COD order placement
            return redirect('place_order_from_cart')
        else:
            # Placeholder — you can add UPI/netbanking handling later
            return redirect('place_order_from_cart')  # or redirect to another page for UPI/netbanking

    return render(request, 'store/checkout_view.html', {'cart_items': cart_items, 'total': total})

# ----------------- BUY NOW + PLACE ORDER -----------------

@login_required
def buy_now(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/buy_now.html', {'product': product})

@login_required
def place_order(request, slug):
    product = get_object_or_404(Product, slug=slug)

    if request.method == "POST":
        action = request.POST.get("action")
        payment_method = request.POST.get("payment_method")

        if action == "add-to-cart":
            cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
            if not created:
                cart_item.quantity += 1
                cart_item.save()
            messages.success(request, f"'{product.name}' added to cart.")
            return redirect('cart')

        elif action == "order":
            if payment_method == "Cash on Delivery":
                # TODO: Save order using Order model if needed
                messages.success(request, f"Order placed for {product.name} via {payment_method}.")
                return redirect('product_list')
            else:
                messages.warning(request, f"{payment_method} coming soon.")
                return redirect('buy_now', product.id)

    return render(request, 'store/buy_now.html', {'product': product})

@login_required
def place_order_from_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('cart')

    if request.method == "POST":
        payment_method = request.POST.get("payment_method")
        if payment_method == "Cash on Delivery":
            # TODO: Save orders for each item
            cart_items.delete()
            messages.success(request, "Order placed for all items in cart!")
            return redirect('product_list')
        else:
            messages.warning(request, f"{payment_method} payment method coming soon.")
            return redirect('cart')

    total = sum(item.total_price() for item in cart_items)
    return render(request, 'store/place_order_cart.html', {
        'cart_items': cart_items,
        'total': total,
    })
@login_required
def place_order_page(request, slug=None):
    user = request.user

    if request.method == "POST":
        address = request.POST.get('address')
        payment_method = request.POST.get("payment_method")

        if not address:
            messages.error(request, "Please provide an address.")
            return redirect('place_order_page', slug=slug if slug else '')

        # ✅ Create the order first
        order = Order.objects.create(
            user=user,
            address=address,
            payment_method=payment_method,
            is_paid=False
        )

        if slug:  # ✅ Buy Now (single product)
            product = get_object_or_404(Product, slug=slug)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=1,
                price=product.price
            )
        else:  # ✅ Cart Checkout
            cart_items = CartItem.objects.filter(user=user)
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            cart_items.delete()
        request.session['order_success_shown']= False
        return redirect('order_success')  # or your order summary/account page
    return render(request,'store/order_success.html')

@login_required
def order_success(request):
    # Only show animation if it's not shown already
    show_animation = not request.session.get('order_success_shown', False)

    context = {
        'show_animation': show_animation,
        'order_already_placed': not show_animation,
    }

    # ✅ Now set the flag only when animation is about to show
    if show_animation:
        request.session['order_success_shown'] = True

    return render(request, 'store/order_success.html', context)
@csrf_exempt
def reset_animation(request):
    if request.method=='POST':
        request.session['order_success_shown']=False
        return jsonResponse({'status':'reset'})

# ----------------- LOGIN / SIGNUP -----------------

def login_signup_view(request):
    if request.method == 'POST':
        # LOGIN
        if 'login' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('account')
            else:
                messages.error(request, "Invalid login credentials.")

        # SIGNUP
        elif 'signup' in request.POST:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            age = request.POST.get('age')
            gender = request.POST.get('gender')
            address = request.POST.get('address')
            mobile = request.POST.get('mobile')

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                Profile.objects.create(user=user, age=age, gender=gender, address=address, mobile=mobile)
                messages.success(request, 'Signup successful. Please log in.')
                return redirect('login_signup')

    return render(request, 'store/login_signup.html')


# ----------------- ACCOUNT & PROFILE -----------------

@login_required
def account_view(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'store/account.html', {'profile': profile})

@login_required
def edit_account(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()

        profile.age = request.POST.get('age')
        profile.gender = request.POST.get('gender')
        profile.address = request.POST.get('address')
        profile.mobile = request.POST.get('mobile_number')
        profile.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('account')

    return render(request, 'store/edit_account.html', {'profile': profile})


# ----------------- LOGOUT -----------------

def logout_view(request):
    logout(request)
    return redirect('login_signup')