from rest_framework import serializers
from .models import Car, Comment


# Сериалайзер для записей об автомобилях
class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'
        read_only_fields = ['author', 'id']


# Сериалайзер для комментариев к записям об автомобилях
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']