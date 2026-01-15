#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_project.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from store.models import Category

# Delete empty categories
Category.objects.filter(product__isnull=True).delete()

# Verify
print("\nFinal categories:")
for cat in Category.objects.all().order_by('order'):
    count = cat.product_set.count()
    print(f"  {cat.id}. {cat.name} ({count} items)")
