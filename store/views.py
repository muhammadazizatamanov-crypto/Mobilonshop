from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category


def homepage(request):
    """Главная страница магазина"""
    context = {
        'categories': Category.objects.filter(show_on_homepage=True),
        'popular_products': Product.objects.filter(
            is_popular=True,
            available=True,
            show_on_homepage=True
        )[:6],
        'new_products': Product.objects.filter(
            available=True,
            show_on_homepage=True
        ).order_by('-created_at')[:6],
    }
    return render(request, 'store/homepage.html', context)


def category_list(request):
    """Список всех категорий"""
    categories = Category.objects.all()
    return render(request, 'store/category_list.html', {'categories': categories})


def category_products(request, category_id):
    """Товары в категории"""
    category = get_object_or_404(Category, id=category_id)
    products = category.product_set.filter(available=True).order_by('-is_popular', '-created_at')
    
    # Поиск
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(brand__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    context = {
        'category': category,
        'categories': Category.objects.all(),
        'products': products,
        'search_query': search_query,
    }
    return render(request, 'store/category_products.html', context)


def product_list(request):
    """Список всех товаров (для простой навигации)"""
    products = Product.objects.filter(available=True).order_by('-is_popular', '-created_at')
    
    # Фильтры
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category', '')
    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(brand__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    if category_id:
        products = products.filter(category_id=category_id)
    
    context = {
        'products': products,
        'categories': Category.objects.all(),
        'search_query': search_query,
        'selected_category': category_id,
    }
    return render(request, 'store/product_list.html', context)


def product_detail(request, pk):
    """Страница товара"""
    product = get_object_or_404(Product, pk=pk)
    product.increment_views()  # Увеличиваем счётчик просмотров
    
    # Похожие товары (в той же категории)
    similar_products = Product.objects.filter(
        category=product.category,
        available=True
    ).exclude(pk=pk)[:4]
    
    context = {
        'product': product,
        'categories': Category.objects.all(),
        'similar_products': similar_products,
        'discount_percent': product.get_discount_percent(),
        'whatsapp_number': '+996550179400',  # Номер для WhatsApp
        'phone_number': '0550 179 400',  # Номер телефона
    }
    return render(request, 'store/product_detail.html', context)
