# Mobilon - Minimal Django Shop

Quick start:

1. Create and activate a virtualenv (optional but recommended).

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
```

2. Install requirements:

```bash
pip install -r requirements.txt
```

3. Apply migrations and create superuser:

```bash
python manage.py migrate
python manage.py createsuperuser
```

4. Run server:

```bash
python manage.py runserver
```

5. Open Admin at `http://127.0.0.1:8000/admin/` to add products (recommended).

Project layout created for a minimal shop with a `store` app.
