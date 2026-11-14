# Aýakgap dükany (Django)

## Işletmek
    python -m venv venv
    source venv/bin/activate        # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py seed           # demo önümler + admin (admin / admin12345)
    python manage.py runserver

Sahypa: http://127.0.0.1:8000/   Admin: http://127.0.0.1:8000/admin/

Täze önümleri admin panelden suratlary bilen goşup bilersiňiz.
Production üçin SECRET_KEY we DEBUG=False üýtgediň, admin paroly çalyşyň.
