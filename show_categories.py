#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_project.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from store.models import Category

categories = Category.objects.all().order_by('order')
print("\n[CATEGORIES]")
for cat in categories:
    print(f"  {cat.id}. {cat.name} (icon: {cat.icon})")
