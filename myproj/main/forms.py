from .models import Car, Comment
from django.forms import ModelForm
from django import forms


# Шаблон формы для автомобилей
class CarForm(ModelForm):
    class Meta:
        model = Car
        fields = ["make", "model", "year", "description"]


# Шаблон формы для комментариев
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Добавьте свой комментарий...'}),
        }