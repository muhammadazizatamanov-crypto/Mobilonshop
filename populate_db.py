#!/usr/bin/env python
"""
Скрипт для заполнения БД тестовыми категориями и товарами
Используйте: python manage.py shell < populate_db.py
"""

from store.models import Category, Product

# Очищаем старые данные (опционально)
# Category.objects.all().delete()
# Product.objects.all().delete()

# Создаём категории
categories_data = [
    ("📱 Телефоны", "📱", 1),
    ("💻 Ноутбуки", "💻", 2),
    ("📺 Телевизоры", "📺", 3),
    ("❄️ Холодильники", "❄️", 4),
    ("🧺 Стиральные машины", "🧺", 5),
    ("🍳 Духовки и микроволновки", "🍳", 6),
    ("🧹 Пылесосы", "🧹", 7),
    ("🔥 Утюги", "🔥", 8),
    ("⌚ Часы", "⌚", 9),
    ("♨️ Tefal", "♨️", 10),
    ("🏠 Ariston", "🏠", 11),
]

categories = {}
for name, icon, order in categories_data:
    cat, created = Category.objects.get_or_create(
        name=name,
        defaults={'icon': icon, 'order': order, 'show_on_homepage': True}
    )
    categories[name] = cat
    if created:
        print(f"✓ Создана категория: {name}")
    else:
        print(f"✓ Категория уже существует: {name}")

# Товары
products_data = [
    # Телефоны (популярные)
    {
        "name": "iPhone 17 Pro Max",
        "category": "📱 Телефоны",
        "price": 145000,
        "old_price": 160000,
        "description": "Флагманский смартфон Apple с экраном 6.9 дюймов, процессором A19 Pro, 512GB памяти. Face ID, лучшая камера в мире.",
        "brand": "Apple",
        "available": True,
        "is_popular": True,
        "show_on_homepage": True,
    },
    {
        "name": "Samsung Galaxy S25 Ultra",
        "category": "📱 Телефоны",
        "price": 135000,
        "old_price": 150000,
        "description": "Мощный флагман Samsung с экраном AMOLED 6.8 дюймов, Snapdragon 8 Elite. Отличная батарея на целый день.",
        "brand": "Samsung",
        "available": True,
        "is_popular": True,
        "show_on_homepage": True,
    },
    {
        "name": "Xiaomi 14 Ultra",
        "category": "📱 Телефоны",
        "price": 85000,
        "old_price": None,
        "description": "Отличное соотношение цены и качества. Snapdragon 8 Gen 3, 256GB памяти. Камеры Leica.",
        "brand": "Xiaomi",
        "available": True,
        "is_popular": False,
        "show_on_homepage": True,
    },
    
    # Ноутбуки
    {
        "name": "MacBook Pro 16\" M4",
        "category": "💻 Ноутбуки",
        "price": 320000,
        "old_price": 350000,
        "description": "Мощный ноутбук для профессионалов. 16-дюймовый Retina дисплей, 512GB SSD, 16GB RAM. Идеален для видеомонтажа и дизайна.",
        "brand": "Apple",
        "available": True,
        "is_popular": True,
        "show_on_homepage": True,
    },
    {
        "name": "ASUS VivoBook 15 Pro",
        "category": "💻 Ноутбуки",
        "price": 95000,
        "old_price": None,
        "description": "Легкий и компактный ноутбук для учёбы и работы. Intel i7, 512GB SSD, 16GB RAM, батарея на 12 часов.",
        "brand": "ASUS",
        "available": True,
        "is_popular": False,
        "show_on_homepage": True,
    },
    {
        "name": "Dell XPS 13 Plus",
        "category": "💻 Ноутбуки",
        "price": 115000,
        "old_price": None,
        "description": "Ультратонкий ноутбук в минималистичном дизайне. Intel Core Ultra 7, 512GB SSD. Идеален для путешествий.",
        "brand": "Dell",
        "available": True,
        "is_popular": True,
        "show_on_homepage": True,
    },
    
    # Телевизоры
    {
        "name": "Samsung QLED 65\" 4K",
        "category": "📺 Телевизоры",
        "price": 185000,
        "old_price": 210000,
        "description": "Потрясающий 4K QLED телевизор с квантовыми точками. 120Hz, Smart TV, встроенный Wi-Fi, отличный звук.",
        "brand": "Samsung",
        "available": True,
        "is_popular": True,
        "show_on_homepage": True,
    },
    {
        "name": "LG OLED 55\" 4K",
        "category": "📺 Телевизоры",
        "price": 175000,
        "old_price": 200000,
        "description": "Премиум OLED с идеальными чёрными цветами. WebOS Smart TV, 4K, 120Hz. Кинематографичная картинка.",
        "brand": "LG",
        "available": True,
        "is_popular": False,
        "show_on_homepage": True,
    },
    
    # Холодильники
    {
        "name": "Ariston RF432 XEF",
        "category": "❄️ Холодильники",
        "price": 125000,
        "old_price": None,
        "description": "Встраиваемый холодильник премиум класса. No Frost, A+ энергоэффективность, вместительная камера с автоматической влажностью.",
        "brand": "Ariston",
        "available": True,
        "is_popular": True,
        "show_on_homepage": True,
    },
    {
        "name": "LG GN-C1052F",
        "category": "❄️ Холодильники",
        "price": 98000,
        "old_price": None,
        "description": "Двухкамерный холодильник с большой морозильной камерой. Экономный по электричеству, вместительный.",
        "brand": "LG",
        "available": True,
        "is_popular": False,
        "show_on_homepage": True,
    },
    
    # Стиральные машины
    {
        "name": "Samsung WW12T504DWH/UA",
        "category": "🧺 Стиральные машины",
        "price": 85000,
        "old_price": 95000,
        "description": "Стиральная машина с инверторным мотором. 12кг вместимости, 1400 оборотов, EcoBubble технология.",
        "brand": "Samsung",
        "available": True,
        "is_popular": False,
        "show_on_homepage": True,
    },
    {
        "name": "Ariston WMUF 5050 L",
        "category": "🧺 Стиральные машины",
        "price": 72000,
        "old_price": None,
        "description": "Надёжная машинка-автомат. 5 кг, 1000 оборотов, энергоэффективная, компактная.",
        "brand": "Ariston",
        "available": True,
        "is_popular": True,
        "show_on_homepage": True,
    },
    
    # Духовки
    {
        "name": "Tefal Ingenio Grand Pro L2799172",
        "category": "🍳 Духовки и микроволновки",
        "price": 18000,
        "old_price": None,
        "description": "Набор посуды из стали с антипригарным покрытием. 20 предметов, подходит для всех плит и духовки.",
        "brand": "Tefal",
        "available": True,
        "is_popular": False,
        "show_on_homepage": True,
    },
    {
        "name": "LG NeoChef MWO2406W",
        "category": "🍳 Духовки и микроволновки",
        "price": 42000,
        "old_price": 48000,
        "description": "Компактная микроволновая печь 20 литров. 800W, 6 уровней мощности, удобное управление.",
        "brand": "LG",
        "available": True,
        "is_popular": False,
        "show_on_homepage": True,
    },
    
    # Пылесосы
    {
        "name": "Dyson V15 Detect",
        "category": "🧹 Пылесосы",
        "price": 125000,
        "old_price": 145000,
        "description": "Премиум беспроводной пылесос. Лазерная технология обнаружения пыли, фильтр HEPA, батарея 60 минут.",
        "brand": "Dyson",
        "available": True,
        "is_popular": True,
        "show_on_homepage": True,
    },
    {
        "name": "Samsung Jet Stick Pet",
        "category": "🧹 Пылесосы",
        "price": 89000,
        "old_price": None,
        "description": "Беспроводной пылесос для тех, у кого есть питомцы. Мощное всасывание, легкий, батарея 40 минут.",
        "brand": "Samsung",
        "available": True,
        "is_popular": False,
        "show_on_homepage": True,
    },
    
    # Утюги
    {
        "name": "Tefal FV5812E0",
        "category": "🔥 Утюги",
        "price": 12500,
        "old_price": None,
        "description": "Утюг с паром 3000W. Быстрый нагрев, гладкая подошва, встроенный отпариватель.",
        "brand": "Tefal",
        "available": True,
        "is_popular": False,
        "show_on_homepage": True,
    },
    
    # Часы
    {
        "name": "Apple Watch Series 10",
        "category": "⌚ Часы",
        "price": 35000,
        "old_price": 40000,
        "description": "Смарт-часы с отличным дисплеем. Фитнес-трекер, ЭКГ, датчик кислорода в крови, водостойкие.",
        "brand": "Apple",
        "available": True,
        "is_popular": True,
        "show_on_homepage": True,
    },
    {
        "name": "Samsung Galaxy Watch 6",
        "category": "⌚ Часы",
        "price": 28000,
        "old_price": None,
        "description": "Стильные смарт-часы на Wear OS. 40 часов автономии, множество циферблатов, фитнес-режимы.",
        "brand": "Samsung",
        "available": True,
        "is_popular": False,
        "show_on_homepage": True,
    },
]

for product_data in products_data:
    category = categories[product_data.pop("category")]
    product, created = Product.objects.get_or_create(
        name=product_data["name"],
        category=category,
        defaults={**product_data}
    )
    if created:
        print(f"✓ Создан товар: {product.name}")
    else:
        print(f"✓ Товар уже существует: {product.name}")

print("\n✅ База данных успешно заполнена!")
print(f"Категорий: {Category.objects.count()}")
print(f"Товаров: {Product.objects.count()}")
