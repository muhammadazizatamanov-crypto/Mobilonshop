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
    except:
        return None

# Last TV image
url = "https://images.pexels.com/photos/3587478/pexels-photo-3587478.jpeg"

try:
    product = Product.objects.get(id=8)
    print(f"[FIX] {product.name}...", end=" ", flush=True)
    
    img_data = download_image_from_url(url)
    
    if img_data:
        filename = f"8_lg_oled_55_4k.jpg"
        product.image.save(filename, ContentFile(img_data.getvalue()), save=True)
        print("[OK]")
    else:
        print("[FAILED]")
        
except Exception as e:
    print(f"[ERROR] {str(e)}")
