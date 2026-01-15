🔧 **TECHNICAL REFERENCE - MOBILON**

## 📁 Структура файлов

```
mobilon/
├── manage.py                      # Django CLI
├── populate_db.py                 # ✨ Скрипт заполнения БД
├── requirements.txt               # 📦 Зависимости
├── db.sqlite3                     # 💾 База данных
│
├── shop_project/                  # ⚙️ Конфиг проекта
│   ├── settings.py
│   ├── urls.py                    # Главные маршруты
│   ├── wsgi.py
│   └── asgi.py
│
├── store/                         # 📦 Главное приложение
│   ├── models.py                  # 📊 Category, Product
│   ├── views.py                   # 👁️ 7 view функций
│   ├── urls.py                    # 🔗 7 маршрутов
│   ├── admin.py                   # ⚙️ Админка
│   ├── apps.py
│   └── migrations/
│       ├── 0001_initial.py        # Первая миграция
│       └── 0002_*.py              # Обновлённые модели
│
├── templates/                     # 🎨 Шаблоны
│   ├── base.html                  # 🔰 Базовый шаблон
│   └── store/
│       ├── homepage.html          # 🏠 Главная
│       ├── product_list.html      # 📦 Все товары
│       ├── product_detail.html    # 🛒 Товар
│       ├── product_card.html      # 🎴 Карточка
│       ├── category_list.html     # 📂 Категории
│       └── category_products.html # 🏪 В категории
│
├── static/                        # 🎨 CSS, JS
│   └── css/
│       └── style.css              # 📄 1000+ строк CSS
│
├── media/                         # 📸 Фото товаров
│   └── products/
│
├── INSTALLATION.md                # 📖 Установка
└── ACTION_PLAN.md                 # 🚀 Дальнейшее развитие
```

---

## 🗄️ МОДЕЛИ ДАННЫХ

### Category (shop_project/store/models.py)

```python
class Category(models.Model):
    name = CharField(max_length=200)           # "Телефоны"
    icon = CharField(max_length=50)            # "📱"
    order = PositiveIntegerField(default=0)    # 1, 2, 3...
    show_on_homepage = BooleanField()          # True/False
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Категории'
```

**Методы:**
- `product_count()` - Количество товаров в категории
- `__str__()` - Возвращает "📱 Телефоны"

---

### Product (shop_project/store/models.py)

```python
class Product(models.Model):
    name = CharField(max_length=200)                    # "iPhone 17 Pro Max"
    price = DecimalField(max_digits=10, decimal_places=2)    # 145000.00
    old_price = DecimalField(..., blank=True, null=True)     # 160000.00 (опционально)
    description = TextField(blank=True)                # Подробное описание
    image = ImageField(upload_to='products/', blank=True, null=True)  # Фото
    category = ForeignKey(Category, on_delete=SET_NULL, null=True)    # Связь с Category
    brand = CharField(max_length=100, blank=True)      # "Apple"
    available = BooleanField(default=True)             # В наличии
    is_popular = BooleanField(default=False)           # Выделить на главной
    show_on_homepage = BooleanField(default=False)     # Показывать на главной
    views_count = PositiveIntegerField(default=0)      # Число просмотров
    created_at = DateTimeField(auto_now_add=True)      # Дата добавления
    
    class Meta:
        ordering = ['-is_popular', '-created_at']
        verbose_name_plural = 'Товары'
```

**Методы:**
- `get_discount_percent()` - Вычислить % скидки
- `increment_views()` - Увеличить счётчик просмотров
- `__str__()` - Возвращает "iPhone 17 Pro Max (145000 сом)"

---

## 👁️ ПРЕДСТАВЛЕНИЯ (Views)

### 1. `homepage(request)` - Главная страница
**URL:** `/` (store:homepage)  
**Шаблон:** `store/homepage.html`

**Контекст:**
```python
{
    'categories': Category.objects.filter(show_on_homepage=True),
    'popular_products': Product.objects.filter(is_popular=True)[:6],
    'new_products': Product.objects.order_by('-created_at')[:6],
}
```

---

### 2. `category_list(request)` - Все категории
**URL:** `/categories/` (store:category_list)  
**Шаблон:** `store/category_list.html`

**Контекст:**
```python
{
    'categories': Category.objects.all(),
}
```

---

### 3. `category_products(request, category_id)` - Товары в категории
**URL:** `/category/<id>/` (store:category_products)  
**Шаблон:** `store/category_products.html`

**Контекст:**
```python
{
    'category': category,
    'categories': Category.objects.all(),
    'products': products,  # Отфильтрованные по поиску
    'search_query': search_query,
}
```

**Фильтры:**
- `?search=iPhone` - Поиск по названию/бренду

---

### 4. `product_list(request)` - Все товары
**URL:** `/all/` (store:product_list)  
**Шаблон:** `store/product_list.html`

**Контекст:**
```python
{
    'products': products,
    'categories': Category.objects.all(),
    'search_query': search_query,
    'selected_category': category_id,
}
```

**Фильтры:**
- `?search=iPhone` - Поиск
- `?category=1` - По категории
- `?search=iPhone&category=1` - Оба параметра

---

### 5. `product_detail(request, pk)` - Страница товара
**URL:** `/product/<id>/` (store:product_detail)  
**Шаблон:** `store/product_detail.html`

**Контекст:**
```python
{
    'product': product,
    'categories': Category.objects.all(),
    'similar_products': similar_products[:4],
    'discount_percent': product.get_discount_percent(),
    'whatsapp_number': '+996550179400',
    'phone_number': '0550 179 400',
}
```

**Эффекты:**
- Автоматически увеличивает `views_count` при открытии

---

## 🔗 URL МАРШРУТЫ

```python
# store/urls.py
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('categories/', views.category_list, name='category_list'),
    path('category/<int:category_id>/', views.category_products, name='category_products'),
    path('all/', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
]
```

**Примеры:**
```
/                       → Главная
/categories/            → Все категории
/category/1/            → Товары категории ID=1
/category/1/?search=... → Поиск в категории
/all/                   → Все товары
/all/?search=...        → Поиск во всех товарах
/all/?category=1        → Фильтр по категории
/product/1/             → Страница товара ID=1
```

---

## 🎨 ШАБЛОНЫ (Templates)

### Иерархия наследования:
```
base.html (базовый шаблон со всем)
├── homepage.html
├── product_list.html
├── product_detail.html
├── category_list.html
└── category_products.html

+ product_card.html (include)
```

### Использование в templates:

```django
{% extends "base.html" %}

{% block title %}Заголовок{% endblock %}

{% block content %}
    <!-- Ваш контент -->
    {% include "store/product_card.html" %}
{% endblock %}
```

### Доступные переменные в шаблонах:

```django
{# Категория #}
{{ category.name }}           → "Телефоны"
{{ category.icon }}           → "📱"
{{ category.product_count }}  → 3

{# Товар #}
{{ product.name }}            → "iPhone 17 Pro Max"
{{ product.price }}           → 145000
{{ product.old_price }}       → 160000
{{ product.image.url }}       → "/media/products/..."
{{ product.brand }}           → "Apple"
{{ product.is_popular }}      → True
{{ product.get_discount_percent }} → 10

{# Условия #}
{% if product.is_popular %}
    ⭐ Популярно!
{% endif %}

{% if product.old_price %}
    Скидка: {{ product.get_discount_percent }}%
{% endif %}

{# Циклы #}
{% for category in categories %}
    {{ category.name }}
{% endfor %}

{# Фильтры #}
{{ product.created_at|date:"d.m.Y" }}  → "15.01.2026"
```

---

## ⚙️ АДМИНКА (Admin)

### CategoryAdmin

**Отображение списка:**
```python
list_display = ('icon', 'name', 'order', 'product_count', 'show_on_homepage')
```

**Редактируемые поля:**
```python
list_editable = ('order', 'show_on_homepage')
```

**Фильтры:**
```python
list_filter = ('show_on_homepage',)
```

**Поиск:**
```python
search_fields = ('name',)
```

### ProductAdmin

**Отображение списка:**
```python
list_display = (
    'name', 'category', 'price', 'old_price', 
    'available', 'is_popular', 'show_on_homepage', 
    'views_count', 'created_at'
)
```

**Редактируемые поля:**
```python
list_editable = ('available', 'is_popular', 'show_on_homepage')
```

**Фильтры:**
```python
list_filter = ('category', 'available', 'is_popular', 'show_on_homepage', 'created_at')
```

**Поиск:**
```python
search_fields = ('name', 'brand', 'description')
```

**Только для чтения:**
```python
readonly_fields = ('views_count', 'created_at')
```

---

## 📊 СТАТИСТИКА БД

### SQL примеры:

```sql
-- Все категории
SELECT * FROM store_category ORDER BY "order";

-- Товары в категории
SELECT * FROM store_product WHERE category_id = 1 ORDER BY -is_popular;

-- Топ 5 популярных товаров
SELECT * FROM store_product 
WHERE is_popular = TRUE 
ORDER BY views_count DESC 
LIMIT 5;

-- Товары со скидками
SELECT * FROM store_product 
WHERE old_price IS NOT NULL;

-- Недоступные товары
SELECT * FROM store_product WHERE available = FALSE;

-- Товары на главной
SELECT * FROM store_product 
WHERE show_on_homepage = TRUE 
ORDER BY -is_popular;
```

### Через Django ORM:

```python
# Все категории
Category.objects.all()

# Товары категории
Product.objects.filter(category_id=1)

# Популярные товары
Product.objects.filter(is_popular=True)

# Товары со скидками
Product.objects.filter(old_price__isnull=False)

# Поиск
Product.objects.filter(
    Q(name__icontains='iPhone') |
    Q(brand__icontains='Apple')
)

# Топ просмотров
Product.objects.order_by('-views_count')[:5]

# Недоступные
Product.objects.filter(available=False)
```

---

## 🎯 ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ

### Добавить категорию программно:

```python
from store.models import Category

Category.objects.create(
    name="🎮 Игровые консоли",
    icon="🎮",
    order=12,
    show_on_homepage=True
)
```

### Добавить товар:

```python
from store.models import Product, Category

category = Category.objects.get(name="📱 Телефоны")
Product.objects.create(
    name="Google Pixel 9 Pro",
    category=category,
    price=120000,
    old_price=135000,
    description="Флагман с лучшей камерой",
    brand="Google",
    available=True,
    is_popular=True,
    show_on_homepage=True,
)
```

### Получить все товары категории:

```python
category = Category.objects.get(id=1)
products = category.product_set.filter(available=True)

for product in products:
    print(f"{product.name} - {product.price} сом")
```

### Увеличить просмотры:

```python
product = Product.objects.get(id=1)
product.increment_views()  # +1 к views_count
```

### Получить скидку в процентах:

```python
product = Product.objects.get(id=1)
discount = product.get_discount_percent()  # Возвращает число
```

---

## 🔒 БЕЗОПАСНОСТЬ

### CSRF защита:
```django
{% csrf_token %}  <!-- В forms -->
```

### XSS защита:
```django
{{ variable|escape }}  <!-- Автоматически -->
```

### SQL Injection защита:
```python
# ❌ Опасно
Product.objects.raw(f"SELECT * WHERE id = {user_input}")

# ✅ Безопасно
Product.objects.filter(id=user_input)
```

---

## 🚀 ПРОИЗВОДИТЕЛЬНОСТЬ

### Оптимизация запросов:

```python
# ❌ N+1 проблема
for product in Product.objects.all():
    print(product.category.name)  # Новый запрос для каждого!

# ✅ Оптимально
for product in Product.objects.select_related('category'):
    print(product.category.name)  # Один запрос
```

### Кэширование:

```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # 5 минут
def homepage(request):
    ...
```

### Пагинация:

```python
from django.core.paginator import Paginator

products = Product.objects.all()
paginator = Paginator(products, 20)  # 20 товаров на странице
page_obj = paginator.get_page(request.GET.get('page'))
```

---

## 📈 МАСШТАБИРОВАНИЕ

### Если много товаров:
1. Добавить Elasticsearch для поиска
2. Использовать Celery для background tasks
3. Добавить Redis для кэша

### Если много пользователей:
1. Миграция с SQLite на PostgreSQL
2. Добавить CDN для static/media
3. Использовать load balancing

### Файл settings.py для production:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mobilon_db',
        'USER': 'postgres',
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': '5432',
    }
}

# Кэш
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}

# Безопасность
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

---

## 🧪 ТЕСТИРОВАНИЕ

### Базовые тесты:

```python
# store/tests.py
from django.test import TestCase, Client
from store.models import Category, Product

class ProductTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test", icon="🔬", order=1)
        self.product = Product.objects.create(
            name="Test Product",
            category=self.category,
            price=100
        )
    
    def test_product_str(self):
        self.assertEqual(str(self.product), "Test Product (100 сом)")
    
    def test_homepage_view(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
```

**Запуск тестов:**
```bash
python manage.py test
python manage.py test store.tests.ProductTestCase
```

---

## 📦 РАЗВЕРТЫВАНИЕ

### Gunicorn + Systemd:

```bash
# Установка
pip install gunicorn

# Запуск
gunicorn shop_project.wsgi:application --bind 0.0.0.0:8000

# Systemd сервис /etc/systemd/system/mobilon.service
[Unit]
Description=Mobilon Shop
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/home/mobilon/
ExecStart=/home/mobilon/venv/bin/gunicorn shop_project.wsgi:application --bind 127.0.0.1:8000

[Install]
WantedBy=multi-user.target
```

### Nginx конфиг:

```nginx
server {
    listen 80;
    server_name mobilon.kg www.mobilon.kg;

    location / {
        proxy_pass http://127.0.0.1:8000;
    }

    location /static/ {
        alias /home/mobilon/static/;
    }

    location /media/ {
        alias /home/mobilon/media/;
    }
}
```

---

✨ **Всё готово к использованию!**
