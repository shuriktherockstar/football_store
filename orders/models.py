import random
import string

from django.core.exceptions import ValidationError

from orders.enums import *
from products.models import *
from users.models import *


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'Корзина пользователя {self.user}'

    def get_cart_items(self):
        return CartItem.objects.filter(cart=self)

    def calculate_total_price(self):
        cart_items = self.get_cart_items()
        self.total_price = sum(item.subtotal() for item in cart_items)
        self.save()

    def clear_cart(self):
        cart_items = self.get_cart_items()
        cart_items.delete()
        self.calculate_total_price()

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class CartItem(models.Model):
    product_unit = models.OneToOneField(ProductUnit, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    def __str__(self):
        return f'Товар {self.product_unit} в корзине пользователя {self.cart.user}'

    def subtotal(self):
        return self.product_unit.product.price * self.quantity

    def clean(self):
        if self.quantity > self.product_unit.quantity:
            raise ValidationError("Количество товаров в корзине не может превышать количество товаров в наличии")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

        self.cart.calculate_total_price()

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=8, unique=True, blank=True, editable=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=255, choices=OrderStatus.get_choices(), verbose_name='статус')
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'Заказ {self.order_number} на сумму {self.total_price}'

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        if not self.total_price:
            self.total_price = 0
        else:
            self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)

    def get_order_items(self):
        return OrderItem.objects.filter(order=self)

    @staticmethod
    def generate_order_number():
        return ''.join(random.choice(string.ascii_letters.upper() + string.digits) for _ in range(8))

    def calculate_total_price(self):
        order_items = self.get_order_items()
        return sum(item.calculate_subtotal() for item in order_items)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    product_unit = models.ForeignKey(ProductUnit, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return f'Товар {self.product_unit} в заказе {self.order.order_number}'

    def calculate_subtotal(self):
        return self.product_unit.product.price * self.quantity

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        order = Order.objects.get(pk=self.order.pk)
        order.total_price = order.calculate_total_price()
        order.save()

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'
