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

# Alternative image sources - High quality product images
product_images = {
    2: "https://images.unsplash.com/photo-1516321314526-1bfe040b8db8?w=500&q=80",  # Samsung Phone
    3: "https://images.unsplash.com/photo-1606933248051-5ce98ae4a426?w=500&q=80",  # Xiaomi
    5: "https://images.unsplash.com/photo-1559056199-641a0ac8b3f7?w=500&q=80",     # ASUS Laptop
    8: "https://images.unsplash.com/photo-1611532736579-6b16e2b50449?w=500&q=80",  # LG OLED TV
}

print("\n[RETRY 2] Adding remaining failed images...\n")

for product_id, url in product_images.items():
    try:
        product = Product.objects.get(id=product_id)
        
        if product.image:
            print(f"[SKIP] {product.name} - already has image")
            continue
        
        print(f"[DL] {product.name}...", end=" ", flush=True)
        
        img_data = download_image_from_url(url)
        
        if not img_data:
            print("[FAIL]")
            continue
        
        filename = f"{product.id}_{product.name.replace(' ', '_').lower()}.jpg"
        product.image.save(filename, ContentFile(img_data.getvalue()), save=True)
        print("[OK]")
        
    except Product.DoesNotExist:
        print(f"[NOT FOUND] Product {product_id}")
    except Exception as e:
        print(f"[ERR] {str(e)}")

print(f"\n[DONE] Refresh http://127.0.0.1:8000/")
