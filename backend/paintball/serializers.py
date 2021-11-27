from rest_framework import serializers
from .models import (
    Brand,
    Image,
    Category,
    Condition,
    Like,
    Comment,
    Item,
)
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',          
            'email',
            'is_staff',
        ]

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = [
            'id', 
            'name',
            'updated_at',
            'created_at',        
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
        'id', 
        'name',
        'updated_at',
        'created_at',
    ]


class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = [
            'id', 
            'name',
            'updated_at',
            'created_at',            
        ]


class CommentReadSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    
    class Meta:
        model = Comment
        fields = [
            'id',
            'comment',
            'user',
            'item',
            'updated_at',
            'created_at',
        ]

class CommentWriteSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Comment
        fields = [
            'id',
            'comment',
            'user',
            'item',            
            'updated_at',
            'created_at',
        ]


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = [
            'id',
            'user',
            'item',
            'updated_at',
            'created_at',
        ]

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = [
            'id',
            'image',
            'item',
            'updated_at',
            'created_at',
        ]

class ItemWriteSerializer(serializers.ModelSerializer):
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
            'created_at'
        ]

class ItemReadSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    comments = CommentReadSerializer(many=True, read_only=True)
    condition = ConditionSerializer(many=False, read_only=True)
    category = CategorySerializer(many=False, read_only=True)
    brand = BrandSerializer(many=False, read_only=True)
    user = UserSerializer(many=False, read_only=True)
    
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
            'images',
            'likes',
            'comments',
            'condition',
            'updated_at',
            'created_at'
        ]


