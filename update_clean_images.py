#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_project.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

import requests
from io import BytesIO
from django.core.files.base import ContentFile
from store.models import Product

def download_image_from_url(url, timeout=10):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return BytesIO(response.content)
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return None

# High-quality product images WITHOUT people
product_images = {
    1: "https://images.unsplash.com/photo-1592286927505-1def25115558?w=500&q=80",  # iPhone
    2: "https://images.unsplash.com/photo-1610945415295-d9bbf7e0b254?w=500&q=80",  # Samsung Phone
    3: "https://images.unsplash.com/photo-1606933248051-5ce98ae4a426?w=500&q=80",  # Xiaomi
    4: "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500&q=80",  # MacBook (no people)
    5: "https://images.unsplash.com/photo-1593642632959-8a47b4f34c4f?w=500&q=80",   # ASUS Laptop
    6: "https://images.unsplash.com/photo-1588871657840-790ff3d952df?w=500&q=80",  # Dell Laptop
    7: "https://images.unsplash.com/photo-1611532736579-6b16e2b50449?w=500&q=80",  # Samsung TV
    8: "https://images.unsplash.com/photo-1559056199-641a0ac8b3f7?w=500&q=80",     # LG OLED TV
    9: "https://images.unsplash.com/photo-1584568694244-14fbdf83bd30?w=500&q=80",  # Ariston Fridge
    10: "https://images.unsplash.com/photo-1608889335941-32ac5f2041c3?w=500&q=80", # LG Fridge
    11: "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=500&q=80",    # Washer
    12: "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=500&q=80",    # Washer
    13: "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=500&q=80",    # Cookware
    14: "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=500&q=80",    # Microwave
    15: "https://images.unsplash.com/photo-1578749556568-bc2c40e68b61?w=500&q=80",  # Vacuum
    16: "https://images.unsplash.com/photo-1578749556568-bc2c40e68b61?w=500&q=80",  # Vacuum
    17: "https://images.unsplash.com/photo-1610701596007-11502861dcfa?w=500&q=80",  # Iron
    18: "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&q=80",  # Watch
    19: "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&q=80",  # Watch
}

print("\n[RELOAD] Updating all product images without people...\n")

products = Product.objects.all()
successful = 0
failed = 0

for product in products:
    url = product_images.get(product.id)
    
    if not url:
        print(f"[SKIP] {product.name} - no URL")
        continue
    
    print(f"[UPDATE] {product.name}...", end=" ", flush=True)
    
    img_data = download_image_from_url(url)
    
    if not img_data:
        print("[FAIL]")
        failed += 1
        continue
    
    try:
        filename = f"{product.id}_{product.name.replace(' ', '_').lower()}.jpg"
        product.image.save(filename, ContentFile(img_data.getvalue()), save=True)
        print("[OK]")
        successful += 1
        
    except Exception as e:
        print(f"[ERR] {str(e)}")
        failed += 1

print(f"\n{'='*50}")
print(f"[SUCCESS] Updated: {successful}")
print(f"[FAILED] Errors: {failed}")
print(f"{'='*50}\n")
