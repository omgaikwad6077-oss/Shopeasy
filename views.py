from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category, Cart, Order, OrderItem

def home(request):
    """Home page view"""
    featured_products = Product.objects.all()[:8]
    categories = Category.objects.all()[:6]
    
    # Get cart count for authenticated users
    cart_count = 0
    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(user=request.user).count()
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
        'cart_count': cart_count,
    }
    return render(request, 'store/home.html', context)

def product_list(request):
    """Product listing page with search and filtering"""
    category_id = request.GET.get('category')
    search_query = request.GET.get('search', '')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort_by = request.GET.get('sort', '')
    
    products = Product.objects.all()
    
    # Filter by category
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Search functionality
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Filter by price range
    if min_price:
        products = products.filter(price__gte=float(min_price))
    if max_price:
        products = products.filter(price__lte=float(max_price))
    
    # Sorting
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    elif sort_by == 'name_asc':
        products = products.order_by('name')
    
    categories = Category.objects.all()
    
    # Get cart count
    cart_count = 0
    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(user=request.user).count()
    
    context = {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
        'search_query': search_query,
        'min_price': min_price,
        'max_price': max_price,
        'sort_by': sort_by,
        'cart_count': cart_count,
    }
    return render(request, 'store/product_list.html', context)

def product_detail(request, product_id):
    """Product detail page view"""
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product_id)[:4]
    
    # Get cart count
    cart_count = 0
    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(user=request.user).count()
    
    context = {
        'product': product,
        'related_products': related_products,
        'cart_count': cart_count,
    }
    return render(request, 'store/product_detail.html', context)

@login_required
def add_to_cart(request, product_id):
    """Add product to cart"""
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        
        # Check if product is in stock
        if product.stock < quantity:
            messages.error(request, f'Sorry, only {product.stock} items available in stock.')
            return redirect('product_detail', product_id=product_id)
        
        # Check if item already in cart
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            # Update quantity if item already in cart
            if cart_item.quantity + quantity > product.stock:
                messages.error(request, f'Cannot add more. Only {product.stock - cart_item.quantity} more available.')
                return redirect('product_detail', product_id=product_id)
            
            cart_item.quantity += quantity
            cart_item.save()
            messages.success(request, f'Updated quantity of {product.name} in cart!')
        else:
            messages.success(request, f'Added {product.name} to cart!')
        
        return redirect('cart')
    
    # If not POST request, redirect to product detail
    return redirect('product_detail', product_id=product_id)

@login_required
def cart(request):
    """View shopping cart"""
    cart_items = Cart.objects.filter(user=request.user)
    
    # Calculate totals
    subtotal = sum(item.product.price * item.quantity for item in cart_items)
    shipping = 0 if subtotal >= 50 else 5.00  # Free shipping over $50
    tax = subtotal * 0.10  # 10% tax
    total = subtotal + shipping + tax
    
    # Get cart count
    cart_count = cart_items.count()
    
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'tax': tax,
        'total': total,
        'cart_count': cart_count,
    }
    return render(request, 'store/cart.html', context)

@login_required
def update_cart_item(request, item_id):
    """Update cart item quantity"""
    if request.method == 'POST':
        cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity < 1:
            cart_item.delete()
            messages.success(request, 'Item removed from cart.')
        elif quantity > cart_item.product.stock:
            messages.error(request, f'Only {cart_item.product.stock} available in stock.')
        else:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated.')
        
        return redirect('cart')
    
    return redirect('cart')

@login_required
def remove_cart_item(request, item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('cart')

@login_required
def checkout(request):
    """Checkout page"""
    cart_items = Cart.objects.filter(user=request.user)
    
    if not cart_items:
        messages.warning(request, 'Your cart is empty!')
        return redirect('product_list')
    
    # Calculate totals
    subtotal = sum(item.product.price * item.quantity for item in cart_items)
    shipping = 0 if subtotal >= 50 else 5.00
    tax = subtotal * 0.10
    total = subtotal + shipping + tax
    
    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        shipping_address = request.POST.get('shipping_address', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        zip_code = request.POST.get('zip_code', '').strip()
        country = request.POST.get('country', '').strip()
        payment_method = request.POST.get('payment_method', 'credit_card')
        
        # Build full shipping address
        full_address = f"{first_name} {last_name}\n{shipping_address}\n{city}, {state} {zip_code}\n{country}"
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            shipping_address=full_address,
            status='pending'
        )
        
        # Create order items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            
            # Update product stock
            cart_item.product.stock -= cart_item.quantity
            cart_item.product.save()
        
        # Clear cart
        cart_items.delete()
        
        messages.success(request, 'Order placed successfully!')
        return redirect('order_confirmation', order_id=order.id)
    
    # Pre-fill user info if available
    user = request.user
    initial_data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
    }
    
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'tax': tax,
        'total': total,
        'initial_data': initial_data,
        'cart_count': cart_items.count(),
    }
    return render(request, 'store/checkout.html', context)

@login_required
def order_confirmation(request, order_id):
    """Order confirmation page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Calculate totals
    shipping = 0 if order.total_amount >= 50 else 5.00
    tax = order.total_amount * 0.10
    total = order.total_amount + shipping + tax
    
    # Get cart count
    cart_count = Cart.objects.filter(user=request.user).count()
    
    context = {
        'order': order,
        'shipping': shipping,
        'tax': tax,
        'total': total,
        'cart_count': cart_count,
    }
    return render(request, 'store/order_confirmation.html', context)

@login_required
def order_history(request):
    """Order history page"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    # Get cart count
    cart_count = Cart.objects.filter(user=request.user).count()
    
    context = {
        'orders': orders,
        'cart_count': cart_count,
    }
    return render(request, 'store/order_history.html', context)

def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        remember = request.POST.get('remember')
        
        # Try to authenticate
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Set session expiry
            if not remember:
                request.session.set_expiry(0)  # Session expires on browser close
            else:
                request.session.set_expiry(1209600)  # 2 weeks
            
            messages.success(request, 'Logged in successfully!')
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    context = {}
    return render(request, 'store/login.html', context)

def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        terms = request.POST.get('terms')
        
        # Validation
        errors = []
        
        if not username:
            errors.append('Username is required.')
        elif len(username) < 3:
            errors.append('Username must be at least 3 characters.')
        elif User.objects.filter(username=username).exists():
            errors.append('Username is already taken.')
        
        if not email:
            errors.append('Email is required.')
        elif User.objects.filter(email=email).exists():
            errors.append('Email is already registered.')
        
        if not password:
            errors.append('Password is required.')
        elif len(password) < 8:
            errors.append('Password must be at least 8 characters.')
        elif password != confirm_password:
            errors.append('Passwords do not match.')
        
        if not terms:
            errors.append('You must agree to the terms and conditions.')
        
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            # Log the user in
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    
    context = {}
    return render(request, 'store/register.html', context)

def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')

def about(request):
    """About us page"""
    # Get cart count for authenticated users
    cart_count = 0
    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(user=request.user).count()
    
    context = {
        'cart_count': cart_count,
    }
    return render(request, 'store/about.html', context)

def contact(request):
    """Contact us page"""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        
        # Basic validation
        if not name or not email or not subject or not message:
            messages.error(request, 'Please fill in all required fields.')
        elif len(message) < 10:
            messages.error(request, 'Message must be at least 10 characters.')
        else:
            # In a real application, you would:
            # 1. Save to database
            # 2. Send email notification
            # 3. Send confirmation email to user
            
            # For now, just show success message
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('contact')
    
    # Get cart count for authenticated users
    cart_count = 0
    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(user=request.user).count()
    
    context = {
        'cart_count': cart_count,
    }
    return render(request, 'store/contact.html', context)

@login_required
def wishlist(request):
    """Wishlist page (placeholder)"""
    # Note: You need to create a Wishlist model for this to work
    cart_count = Cart.objects.filter(user=request.user).count()
    
    context = {
        'cart_count': cart_count,
    }
    return render(request, 'store/wishlist.html', context)

# Additional utility functions

def get_cart_count(request):
    """Get cart count for any view"""
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user).count()
    return 0

def clear_cart(request):
    """Clear entire cart"""
    if request.user.is_authenticated:
        Cart.objects.filter(user=request.user).delete()
        messages.success(request, 'Cart cleared successfully!')
    return redirect('cart')

@login_required
def cancel_order(request, order_id):
    """Cancel an order"""
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id, user=request.user)
        
        if order.status == 'pending':
            # Update order status
            order.status = 'cancelled'
            order.save()
            
            # Restore product stock
            for item in order.items.all():
                product = item.product
                product.stock += item.quantity
                product.save()
            
            messages.success(request, 'Order cancelled successfully.')
        else:
            messages.error(request, 'Cannot cancel order. Order is already being processed.')
    
    return redirect('order_history')

@login_required
def track_order(request, order_id):
    """Track order status"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Simulate tracking info (in real app, integrate with shipping carrier API)
    tracking_info = {
        'status': order.get_status_display(),
        'tracking_number': f'TRACK{order.id:08d}',
        'estimated_delivery': '2024-12-30',  # Hardcoded for demo
        'carrier': 'USPS',
        'updates': [
            {'date': '2024-12-15', 'time': '10:30 AM', 'status': 'Order Placed', 'location': 'San Francisco, CA'},
            {'date': '2024-12-16', 'time': '2:15 PM', 'status': 'Processing', 'location': 'San Francisco, CA'},
            {'date': '2024-12-17', 'time': '9:45 AM', 'status': 'Shipped', 'location': 'San Francisco, CA'},
        ]
    }
    
    context = {
        'order': order,
        'tracking_info': tracking_info,
        'cart_count': get_cart_count(request),
    }
    return render(request, 'store/track_order.html', context)

# Add this to your urls.py if you want tracking page
# path('orders/track/<int:order_id>/', views.track_order, name='track_order'),
@login_required
def buy_now(request, product_id):
    """Buy Now - Direct checkout for single product"""
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        
        # Check stock
        if product.stock < quantity:
            messages.error(request, f'Sorry, only {product.stock} items available in stock.')
            return redirect('product_detail', product_id=product_id)
        
        # Calculate total
        total = product.price * quantity
        shipping = 0 if total >= 50 else 5.00
        tax = total * 0.10
        grand_total = total + shipping + tax
        
        # Store in session for checkout
        request.session['buy_now_product'] = {
            'product_id': product.id,
            'quantity': quantity,
            'total': float(total),
            'shipping': shipping,
            'tax': float(tax),
            'grand_total': float(grand_total)
        }
        
        # Redirect to express checkout
        return redirect('express_checkout')
    
    return redirect('product_detail', product_id=product_id)

@login_required
def express_checkout(request):
    """Express checkout for Buy Now"""
    if 'buy_now_product' not in request.session:
        messages.error(request, 'No product selected for express checkout.')
        return redirect('product_list')
    
    buy_now_data = request.session['buy_now_product']
    product = get_object_or_404(Product, id=buy_now_data['product_id'])
    
    if request.method == 'POST':
        # Get shipping info
        shipping_address = request.POST.get('shipping_address', '').strip()
        
        if not shipping_address:
            messages.error(request, 'Please provide shipping address.')
            return render(request, 'store/express_checkout.html', {
                'product': product,
                'quantity': buy_now_data['quantity'],
                'total': buy_now_data['total'],
                'shipping': buy_now_data['shipping'],
                'tax': buy_now_data['tax'],
                'grand_total': buy_now_data['grand_total']
            })
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            total_amount=buy_now_data['grand_total'],
            shipping_address=shipping_address,
            status='pending'
        )
        
        # Create order item
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=buy_now_data['quantity'],
            price=product.price
        )
        
        # Update product stock
        product.stock -= buy_now_data['quantity']
        product.save()
        
        # Clear session
        del request.session['buy_now_product']
        
        messages.success(request, 'Order placed successfully!')
        return redirect('order_confirmation', order_id=order.id)
    
    return render(request, 'store/express_checkout.html', {
        'product': product,
        'quantity': buy_now_data['quantity'],
        'total': buy_now_data['total'],
        'shipping': buy_now_data['shipping'],
        'tax': buy_now_data['tax'],
        'grand_total': buy_now_data['grand_total']
    })

@login_required
def add_to_cart(request, product_id):
    """Add product to cart"""
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        
        # Check stock
        if product.stock < quantity:
            messages.error(request, f'Sorry, only {product.stock} items available in stock.')
            return redirect('product_detail', product_id=product_id)
        
        # Check if item already in cart
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            # Update quantity if already in cart
            if cart_item.quantity + quantity > product.stock:
                messages.error(request, f'Cannot add more. Only {product.stock - cart_item.quantity} more available.')
                return redirect('product_detail', product_id=product_id)
            
            cart_item.quantity += quantity
            cart_item.save()
            messages.success(request, f'Updated quantity of {product.name} in cart!')
        else:
            messages.success(request, f'Added {product.name} to cart!')
        
        return redirect('cart')
    
    return redirect('product_detail', product_id=product_id)

@login_required
def update_cart_item(request, item_id):
    """Update cart item quantity"""
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity < 1:
            cart_item.delete()
            messages.success(request, 'Item removed from cart.')
        elif quantity > cart_item.product.stock:
            messages.error(request, f'Only {cart_item.product.stock} available in stock.')
        else:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated.')
    
    return redirect('cart')

@login_required
def remove_cart_item(request, item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('cart')

@login_required
def clear_cart(request):
    """Clear entire cart"""
    Cart.objects.filter(user=request.user).delete()
    messages.success(request, 'Cart cleared successfully!')
    return redirect('cart')

@login_required
def cancel_order(request, order_id):
    """Cancel an order"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status == 'pending':
        order.status = 'cancelled'
        order.save()
        
        # Restore product stock
        for item in order.items.all():
            product = item.product
            product.stock += item.quantity
            product.save()
        
        messages.success(request, 'Order cancelled successfully.')
    else:
        messages.error(request, 'Cannot cancel order. Order is already being processed.')
    
    return redirect('order_history')

def product_quick_view_api(request, product_id):
    """API endpoint for quick view modal"""
    product = get_object_or_404(Product, id=product_id)
    
    data = {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': str(product.price),
        'image_url': product.get_image_url(),
        'category': product.category.name,
        'stock': product.stock,
    }
    
    return JsonResponse(data)

# Add this function if missing
def get_cart_count(request):
    """Get cart count for any view"""
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user).count()
    return 0