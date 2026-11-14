from django import forms
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .cart import Cart
from .models import Order, OrderItem, Product, Category, SIZES

def home(request):
    return render(request, "shop/home.html", {
        "featured": Product.objects.filter(featured=True)[:8],
        "latest": Product.objects.all()[:4],
    })

def product_list(request, slug=None):
    products = Product.objects.select_related("category")
    category = None
    if slug:
        category = get_object_or_404(Category, slug=slug)
        products = products.filter(category=category)
    q = request.GET.get("q", "").strip()
    if q:
        products = products.filter(Q(name__icontains=q) | Q(brand__icontains=q))
    sort = request.GET.get("sort", "")
    products = products.order_by({"cheap": "price", "expensive": "-price"}.get(sort, "-created"))
    return render(request, "shop/list.html", {"products": products, "category": category, "q": q, "sort": sort})

def product_detail(request, slug):
    p = get_object_or_404(Product, slug=slug)
    related = Product.objects.filter(category=p.category).exclude(pk=p.pk)[:4]
    return render(request, "shop/detail.html", {"p": p, "sizes": SIZES, "related": related})

@require_POST
def cart_add(request, pk):
    p = get_object_or_404(Product, pk=pk, in_stock=True)
    size = request.POST.get("size", "")
    if size not in SIZES:
        messages.error(request, "Ölçegi saýlaň.")
        return redirect(p)
    try:
        qty = max(1, min(10, int(request.POST.get("qty", 1))))
    except ValueError:
        qty = 1
    Cart(request).add(p.pk, size, qty)
    messages.success(request, f"“{p.name}” sebede goşuldy.")
    return redirect("cart")

@require_POST
def cart_remove(request, key):
    Cart(request).remove(key)
    return redirect("cart")

def cart_view(request):
    cart = Cart(request)
    return render(request, "shop/cart.html", {"items": cart.items(), "total": cart.total()})

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["name", "phone", "address"]
        widgets = {"address": forms.Textarea(attrs={"rows": 3})}

def checkout(request):
    cart = Cart(request)
    items = cart.items()
    if not items:
        return redirect("cart")
    form = OrderForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        order = form.save(commit=False)
        order.total = cart.total()
        order.save()
        for i in items:
            OrderItem.objects.create(order=order, product=i["product"], size=i["size"],
                                     qty=i["qty"], price=i["product"].price)
        cart.clear()
        return redirect("order_done", pk=order.pk)
    return render(request, "shop/checkout.html", {"form": form, "items": items, "total": cart.total()})

def order_done(request, pk):
    return render(request, "shop/done.html", {"order": get_object_or_404(Order, pk=pk)})
