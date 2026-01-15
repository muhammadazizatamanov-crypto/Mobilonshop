from django.contrib import admin
from .models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('icon', 'name', 'order', 'product_count', 'show_on_homepage')
    list_editable = ('order', 'show_on_homepage')
    list_filter = ('show_on_homepage',)
    search_fields = ('name',)
    ordering = ('order',)
    fieldsets = (
        ('Основное', {
            'fields': ('name', 'icon')
        }),
        ('Отображение', {
            'fields': ('order', 'show_on_homepage')
        }),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'price',
        'old_price',
        'available',
        'is_popular',
        'show_on_homepage',
        'views_count',
        'created_at'
    )
    list_filter = ('category', 'available', 'is_popular', 'show_on_homepage', 'created_at')
    list_editable = ('available', 'is_popular', 'show_on_homepage')
    search_fields = ('name', 'brand', 'description')
    readonly_fields = ('views_count', 'created_at')
    ordering = ('-is_popular', '-created_at')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'category', 'price', 'old_price')
        }),
        ('Описание и медиа', {
            'fields': ('description', 'image'),
            'classes': ('collapse',)
        }),
        ('Характеристики товара', {
            'fields': ('brand', 'available', 'is_popular'),
            'description': 'Выделение и статусы товара'
        }),
        ('Видимость и статистика', {
            'fields': ('show_on_homepage', 'views_count', 'created_at'),
            'description': 'Параметры отображения и просмотров',
            'classes': ('collapse',)
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        """Читать просмотры только для просмотра"""
        if obj:
            return self.readonly_fields
        return []
