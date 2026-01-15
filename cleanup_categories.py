#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_project.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from store.models import Category, Product

print("\n[CLEANUP] Removing extra categories...")

# Товары Tefal -> Духовки и микроволновки
tefal_products = Product.objects.filter(category__name="♨️ Tefal")
if tefal_products.exists():
    cooking_category = Category.objects.filter(name="🍳 Духовки и микроволновки").first()
    if cooking_category:
        for p in tefal_products:
            print(f"[MOVE] {p.name}: ♨️ Tefal -> 🍳 Духовки и микроволновки")
            p.category = cooking_category
            p.save()

# Товары Ariston -> Холодильники и Стиральные машины
ariston_products = Product.objects.filter(category__name="🏠 Ariston")
if ariston_products.exists():
    for p in ariston_products:
        if 'холодильник' in p.name.lower() or 'rf' in p.name.lower():
            fridge_cat = Category.objects.filter(name="❄️ Холодильники").first()
            if fridge_cat:
                print(f"[MOVE] {p.name}: 🏠 Ariston -> ❄️ Холодильники")
                p.category = fridge_cat
                p.save()
        else:
            washer_cat = Category.objects.filter(name="🧺 Стиральные машины").first()
            if washer_cat:
                print(f"[MOVE] {p.name}: 🏠 Ariston -> 🧺 Стиральные машины")
                p.category = washer_cat
                p.save()

# Удаляем категории
tefal = Category.objects.filter(name="♨️ Tefal").first()
if tefal:
    print(f"[DELETE] ♨️ Tefal")
    tefal.delete()

ariston = Category.objects.filter(name="🏠 Ariston").first()
if ariston:
    print(f"[DELETE] 🏠 Ariston")
    ariston.delete()

print(f"\n[DONE] Categories cleaned up!")
print(f"\n[CATEGORIES] Current:")
for cat in Category.objects.all().order_by('order'):
    count = cat.product_set.count()
    print(f"  {cat.id}. {cat.name} ({count} товаров)")
