from decimal import Decimal
from .models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.setdefault("cart", {})

    def add(self, product_id, size, qty=1):
        key = f"{product_id}:{size}"
        self.cart[key] = self.cart.get(key, 0) + qty
        self.session.modified = True

    def remove(self, key):
        self.cart.pop(key, None)
        self.session.modified = True

    def clear(self):
        self.session["cart"] = {}
        self.session.modified = True

    def items(self):
        ids = {k.split(":")[0] for k in self.cart}
        products = {str(p.id): p for p in Product.objects.filter(id__in=ids)}
        out = []
        for key, qty in self.cart.items():
            pid, size = key.split(":")
            p = products.get(pid)
            if p:
                out.append({"key": key, "product": p, "size": size, "qty": qty, "subtotal": p.price * qty})
        return out

    def total(self):
        return sum((i["subtotal"] for i in self.items()), Decimal("0"))

    def count(self):
        return sum(self.cart.values())
