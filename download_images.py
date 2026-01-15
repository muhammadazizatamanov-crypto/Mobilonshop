#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
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
        print(f"Error downloading {url}: {str(e)}")
        return None

def find_and_add_images():
    
    # Словарь товаров с ссылками на красивые фото
    product_images = {
        1: "https://images.unsplash.com/photo-1511707267537-b85faf00021e?w=500&q=80",  # iPhone
        2: "https://images.unsplash.com/photo-1511707267537-b85faf00021e?w=500&q=80",  # Samsung Phone
        3: "https://images.unsplash.com/photo-1511707267537-b85faf00021e?w=500&q=80",  # Xiaomi
        4: "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500&q=80",  # MacBook
        5: "https://images.unsplash.com/photo-1588872657840-790ff3d952df?w=500&q=80",  # ASUS Laptop
        6: "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=500&q=80",  # Dell Laptop
        7: "https://images.unsplash.com/photo-1593642532400-2682a8787205?w=500&q=80",  # Samsung TV
        8: "https://images.unsplash.com/photo-1559056199-641a0ac8b3f7?w=500&q=80",  # LG OLED TV
        9: "https://images.unsplash.com/photo-1584568694244-14fbdf83bd30?w=500&q=80",  # Ariston Fridge
        10: "https://images.unsplash.com/photo-1608889335941-32ac5f2041c3?w=500&q=80",  # LG Fridge
        11: "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=500&q=80",  # Samsung Washer
        12: "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=500&q=80",  # Ariston Washer
        13: "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=500&q=80",  # Tefal Cookware
        14: "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=500&q=80",  # LG Microwave
        15: "https://images.unsplash.com/photo-1578749556568-bc2c40e68b61?w=500&q=80",  # Dyson Vacuum
        16: "https://images.unsplash.com/photo-1578749556568-bc2c40e68b61?w=500&q=80",  # Samsung Vacuum
        17: "https://images.unsplash.com/photo-1610701596007-11502861dcfa?w=500&q=80",  # Tefal Iron
        18: "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&q=80",  # Apple Watch
        19: "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&q=80",  # Samsung Watch
    }
    
    print("\n[+] Starting image download from internet...\n")
    
    products = Product.objects.all()
    successful = 0
    failed = 0
    
    for product in products:
        if product.image:
            print(f"[SKIP] {product.name} - already has image")
            continue
        
        url = product_images.get(product.id)
        
        if not url:
            print(f"[WARN] {product.name} - URL not found")
            continue
        
        print(f"[DOWNLOAD] {product.name}...", end=" ")
        
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
            print(f"[ERROR] {str(e)}")
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"[SUCCESS] Downloaded: {successful}")
    print(f"[FAILED] Errors: {failed}")
    print(f"{'='*50}\n")
    print(f"[INFO] Images saved to: media/products/")
    print(f"[INFO] Open site: http://127.0.0.1:8000/")

if __name__ == '__main__':
    find_and_add_images()
