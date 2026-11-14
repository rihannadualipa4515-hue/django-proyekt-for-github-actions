from .cart import Cart
from .models import Category

def shop_globals(request):
    return {"nav_categories": Category.objects.all(), "cart_count": Cart(request).count()}
