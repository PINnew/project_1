from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

# Модель для цветов
class Flower(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='flowers/')  # Поле для фото

    def __str__(self):
        return f"{self.name} ({self.color}) - {self.price}₽"

# Модель для заказов
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    address = models.TextField()
    comments = models.TextField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)

    def save(self, *args, **kwargs):
        # Автоматически вычисляем стоимость заказа при сохранении
        self.total_price = self.quantity * self.flower.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Заказ {self.id} от {self.user.username}"
