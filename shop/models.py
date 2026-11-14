from django.db import models
from django.urls import reverse

SIZES = [str(s) for s in range(37, 46)]

class Category(models.Model):
    name = models.CharField("Ady", max_length=80)
    slug = models.SlugField(unique=True)
    class Meta:
        verbose_name = "Kategoriýa"
        verbose_name_plural = "Kategoriýalar"
    def __str__(self): return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", verbose_name="Kategoriýa")
    name = models.CharField("Ady", max_length=150)
    slug = models.SlugField(unique=True)
    brand = models.CharField("Brend", max_length=80, blank=True)
    price = models.DecimalField("Bahasy (TMT)", max_digits=10, decimal_places=2)
    old_price = models.DecimalField("Köne bahasy", max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField("Beýany", blank=True)
    image = models.ImageField("Surat", upload_to="products/")
    featured = models.BooleanField("Esasy sahypada", default=False)
    in_stock = models.BooleanField("Bar", default=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-created"]
        verbose_name = "Önüm"
        verbose_name_plural = "Önümler"
    def __str__(self): return self.name
    def get_absolute_url(self): return reverse("product_detail", args=[self.slug])
    @property
    def discount(self):
        if self.old_price and self.old_price > self.price:
            return int(100 - self.price * 100 / self.old_price)
        return 0

class Order(models.Model):
    name = models.CharField("Ady", max_length=120)
    phone = models.CharField("Telefon", max_length=30)
    address = models.TextField("Adres")
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-created"]
        verbose_name = "Sargyt"
        verbose_name_plural = "Sargytlar"
    def __str__(self): return f"Sargyt #{self.pk} - {self.name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    size = models.CharField(max_length=5)
    qty = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self): return f"{self.product} ({self.size}) x{self.qty}"
