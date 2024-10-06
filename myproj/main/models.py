import datetime

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Car(models.Model):
    make = models.CharField("Марка", max_length=32)
    model = models.CharField("Модель", max_length=32)
    year = models.PositiveIntegerField("Год выпуска", blank=True, null=True,
                                       validators=[MinValueValidator(1888), MaxValueValidator(datetime.date.today().year)
                                                   ])
    description = models.TextField("Описание")
    created_at = models.DateTimeField("Создана", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлена", auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.make} {self.model} {self.year}, {self.author}"


    def get_absolute_url(self):
        return f"/cars"

    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural="Автомобили"


class Comment(models.Model):
    content = models.TextField("Содержимое")
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author.username}\n{self.content}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

