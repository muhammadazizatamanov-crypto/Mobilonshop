#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_project.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from store.models import Product

products = Product.objects.all()
total = products.count()
with_images = products.exclude(image__exact="").count()

print(f"\n[STATS]")
print(f"Total products: {total}")
print(f"With images: {with_images}")
print(f"Without images: {total - with_images}\n")

print("[LIST]")
for p in products:
    status = "YES" if p.image else "NO"
    print(f"  {p.id}. {p.name}: {status}")
