from django.db import models


class Category(models.Model):
    """Категория товаров"""
    name = models.CharField(max_length=200, unique=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Emoji иконка, например: 📱")
    order = models.PositiveIntegerField(default=0, help_text="Порядок отображения (0 - сверху)")
    show_on_homepage = models.BooleanField(default=True, help_text="Показывать на главной странице")

    class Meta:
        ordering = ['order']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f"{self.icon} {self.name}"

    def product_count(self):
        return self.product_set.filter(available=True).count()


class Product(models.Model):
    """Товар в магазине"""
    name = models.CharField(max_length=200, verbose_name='Название')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    old_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Старая цена (для скидок)'
    )
    description = models.TextField(blank=True, verbose_name='Описание')
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        verbose_name='Фото товара'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    brand = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Бренд',
        help_text='Например: Tefal, Ariston'
    )
    available = models.BooleanField(default=True, verbose_name='Наличие')
    is_popular = models.BooleanField(default=False, verbose_name='Популярный товар')
    show_on_homepage = models.BooleanField(default=False, verbose_name='Показывать на главной')
    views_count = models.PositiveIntegerField(default=0, verbose_name='Просмотров')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        ordering = ['-is_popular', '-created_at']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f"{self.name} ({self.price} сом)"

    def get_discount_percent(self):
        """Вычислить процент скидки"""
        if self.old_price and self.old_price > self.price:
            return int((self.old_price - self.price) / self.old_price * 100)
        return 0

    def increment_views(self):
        """Увеличить счётчик просмотров"""
        self.views_count += 1
        self.save(update_fields=['views_count'])
