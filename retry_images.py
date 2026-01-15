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
        return None

# Retry with different sources for failed items
product_images = {
    2: "https://images.pexels.com/photos/699122/pexels-photo-699122.jpeg?w=500",    # Samsung Phone
    3: "https://images.pexels.com/photos/699122/pexels-photo-699122.jpeg?w=500",    # Xiaomi
    5: "https://images.pexels.com/photos/18105/pexels-photo.jpg?w=500",             # Laptop
    6: "https://images.pexels.com/photos/18105/pexels-photo.jpg?w=500",             # Laptop
    8: "https://images.pexels.com/photos/1201918/pexels-photo-1201918.jpeg?w=500", # TV
    10: "https://images.pexels.com/photos/1350789/pexels-photo-1350789.jpeg",      # Fridge
}

print("\n[RETRY] Fixing failed images...\n")

for product_id, url in product_images.items():
    try:
        product = Product.objects.get(id=product_id)
        print(f"[FIX] {product.name}...", end=" ", flush=True)
        
        img_data = download_image_from_url(url)
        
        if not img_data:
            print("[SKIP - URL failed]")
            continue
        
        filename = f"{product.id}_{product.name.replace(' ', '_').lower()}.jpg"
        product.image.save(filename, ContentFile(img_data.getvalue()), save=True)
        print("[OK]")
        
    except Product.DoesNotExist:
        print("[NOT FOUND]")
    except Exception as e:
        print(f"[ERROR] {str(e)}")

print(f"\n[DONE]")
