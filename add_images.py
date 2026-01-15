#!/usr/bin/env python
"""
Скрипт для создания и загрузки фото товаров
Использует PIL для создания красивых placeholder изображений
"""

import os
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.core.files.base import ContentFile
from store.models import Product

# Цвета для разных категорий
COLORS = {
    "📱 Телефоны": "#2563eb",           # Синий
    "💻 Ноутбуки": "#7c3aed",            # Фиолетовый
    "📺 Телевизоры": "#dc2626",          # Красный
    "❄️ Холодильники": "#0891b2",        # Голубой
    "🧺 Стиральные машины": "#059669",   # Зелёный
    "🍳 Духовки и микроволновки": "#ea580c", # Оранжевый
    "🧹 Пылесосы": "#6366f1",            # Индиго
    "🔥 Утюги": "#ec4899",               # Розовый
    "⌚ Часы": "#a16207",                 # Коричневый
    "♨️ Tefal": "#047857",                # Изумруд
    "🏠 Ariston": "#7f1d1d",              # Тёмный красный
}

def create_product_image(product_name, category_name, width=400, height=400):
    """
    Создаёт красивое изображение для товара
    """
    # Получаем цвет по категории
    color = COLORS.get(category_name, "#2563eb")
    
    # Конвертируем hex в RGB
    color_rgb = tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    
    # Создаём изображение
    img = Image.new('RGB', (width, height), color_rgb)
    draw = ImageDraw.Draw(img)
    
    # Пытаемся использовать красивый шрифт
    try:
        font_large = ImageFont.truetype("arial.ttf", 60)
        font_small = ImageFont.truetype("arial.ttf", 30)
    except:
        # Если нет шрифта, используем стандартный
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Рисуем текст
    text_y = height // 2 - 60
    
    # Название товара
    draw.text(
        (width // 2, text_y),
        product_name[:25],  # Максимум 25 символов
        fill='white',
        font=font_large,
        anchor='mm'
    )
    
    # Категория
    draw.text(
        (width // 2, text_y + 80),
        category_name,
        fill='rgba(255, 255, 255, 0.8)',
        font=font_small,
        anchor='mm'
    )
    
    return img

def add_images_to_products():
    """
    Добавляет фото ко всем товарам
    """
    products = Product.objects.all()
    
    print(f"\n🖼️ Добавляю фото для {products.count()} товаров...\n")
    
    for i, product in enumerate(products, 1):
        if product.image:
            print(f"⏭️  {i}. {product.name} - уже имеет фото")
            continue
        
        try:
            # Создаём изображение
            img = create_product_image(
                product.name,
                str(product.category)
            )
            
            # Конвертируем в байты
            img_io = BytesIO()
            img.save(img_io, format='PNG')
            img_io.seek(0)
            
            # Сохраняем в модель
            filename = f"{product.id}_{product.name.replace(' ', '_').lower()}.png"
            product.image.save(
                filename,
                ContentFile(img_io.getvalue()),
                save=True
            )
            
            print(f"✅ {i}. {product.name} - фото добавлено!")
            
        except Exception as e:
            print(f"❌ {i}. {product.name} - ошибка: {str(e)}")
    
    print(f"\n✨ Все фото добавлены!")
    print(f"📸 Фото сохранены в: {os.path.join(os.getcwd(), 'media', 'products')}")

if __name__ == '__main__':
    add_images_to_products()
