def cart_context(request):
    """Add cart count to all templates"""
    cart_count = 0
    if request.user.is_authenticated:
        cart_count = request.user.cart_set.count()  # Using default related name
    return {'cart_count': cart_count}