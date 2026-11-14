from decimal import Decimal
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from shop.models import Category, Product

def shoe_svg(c1, c2, bg1, bg2, boot=False):
    top = 120 if boot else 170
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 450">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{bg1}"/><stop offset="1" stop-color="{bg2}"/></linearGradient></defs>
<rect width="600" height="450" fill="url(#g)"/>
<ellipse cx="310" cy="378" rx="250" ry="22" fill="#000" opacity=".18"/>
<path d="M80 305 L80 {top+45} Q80 {top+20} 112 {top+15} L215 {top} Q250 {top-50} 300 {top-20} L330 {top+20} Q420 {top+30} 500 255 Q552 285 548 305 Z" fill="{c1}"/>
<path d="M430 {top+45} Q520 250 548 305 L400 305 Q420 260 430 {top+45}Z" fill="{c2}"/>
<path d="M120 285 Q250 240 380 270" stroke="{c2}" stroke-width="16" fill="none" stroke-linecap="round"/>
<g stroke="#fff" stroke-width="7" stroke-linecap="round" opacity=".9">
<line x1="262" y1="{top+18}" x2="292" y2="{top+48}"/><line x1="290" y1="{top+5}" x2="322" y2="{top+38}"/><line x1="318" y1="{top+22}" x2="350" y2="{top+50}"/></g>
<path d="M66 305 L552 305 L552 330 Q548 362 500 362 L112 362 Q66 362 66 330 Z" fill="#fff"/>
<path d="M66 330 L552 330" stroke="#ddd" stroke-width="5"/>
</svg>'''

DATA = [
 ("sport", "Sport aýakgaplar", [
  ("Air Runner Pro", "Nova", "389", "459", "#ef4444", "#111827", "#fde68a", "#fb923c", False, True),
  ("Speed Max", "Nova", "425", None, "#2563eb", "#f8fafc", "#bfdbfe", "#93c5fd", False, True),
  ("Urban Flex", "Stride", "340", "390", "#10b981", "#064e3b", "#d1fae5", "#6ee7b7", False, False),
  ("Neon Pulse", "Stride", "365", None, "#a855f7", "#fde047", "#f3e8ff", "#d8b4fe", False, True),
 ]),
 ("classic", "Klassyk aýakgaplar", [
  ("Oxford Elegance", "Bella", "520", "600", "#78350f", "#451a03", "#fef3c7", "#fcd34d", False, True),
  ("Business Black", "Bella", "480", None, "#111827", "#374151", "#e5e7eb", "#9ca3af", False, False),
  ("Loafer Classic", "Bella", "450", "510", "#92400e", "#b45309", "#ffedd5", "#fdba74", False, True),
  ("Milan Brown", "Gentry", "540", None, "#7c2d12", "#431407", "#fee2e2", "#fca5a5", False, False),
 ]),
 ("boots", "Gyşky botlar", [
  ("Winter Trek", "Arctic", "610", "720", "#475569", "#0f172a", "#e0f2fe", "#7dd3fc", True, True),
  ("Mountain Boot", "Arctic", "650", None, "#854d0e", "#1c1917", "#fef9c3", "#fde047", True, False),
  ("City Chelsea", "Gentry", "560", "630", "#1f2937", "#d97706", "#f1f5f9", "#cbd5e1", True, False),
  ("Snow Rider", "Arctic", "690", None, "#dc2626", "#1e293b", "#fff1f2", "#fda4af", True, True),
 ]),
]

DESC = ("Ýokary hilli material, ýumşak içki we çydamly aýak aşagy. Uzak wagtlap geýmek üçin amatly. "
        "Ölçegler 37-den 45-e çenli. Gapdaly eltip bermek we töleg alnanda tölemek mümkin.")

class Command(BaseCommand):
    help = "Demo maglumatlary we admin hasabyny döredýär"
    def handle(self, *a, **kw):
        from django.utils.text import slugify
        for slug, cname, items in DATA:
            cat, _ = Category.objects.get_or_create(slug=slug, defaults={"name": cname})
            for name, brand, price, old, c1, c2, b1, b2, boot, feat in items:
                pslug = slugify(name)
                if Product.objects.filter(slug=pslug).exists():
                    continue
                p = Product(category=cat, name=name, slug=pslug, brand=brand, price=Decimal(price),
                            old_price=Decimal(old) if old else None, description=DESC, featured=feat)
                p.image.save(f"{pslug}.svg", ContentFile(shoe_svg(c1, c2, b1, b2, boot).encode()), save=False)
                p.save()
        User = get_user_model()
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "admin12345")
        self.stdout.write(self.style.SUCCESS("Taýyn! Admin: admin / admin12345"))
