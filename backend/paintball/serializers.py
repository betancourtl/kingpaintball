from rest_framework import serializers
from .models import (
    Brand,
    Category,
    Condition,
    Like,
    Comment,
    Item,
)


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'updated_at', 'created']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'updated_at', 'created']


class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = ['id', 'name', 'updated_at', 'created']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'comment',
            'item',
            'user',
            'updated_at',
            'created'
        ]


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = [
            'id',
            'item',
            'user',
            'updated_at',
            'created'
        ]


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = [
            'id',
            'title',
            'sold',
            'description',
            'year',
            'price',
            'category',
            'brand',
            'user',
            'condition',
            'updated_at',
            'created'
        ]
