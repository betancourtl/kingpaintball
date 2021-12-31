from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from paintball.models import (
    Brand,
    Image,
    Category,
    Condition,
    Like,
    Comment,
    Item,
)
from user.serializers import (
    UserSerializer
)
User = get_user_model()


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        read_only_fields = [
            'id',
            'updated_at',
            'created_at',
        ]
        fields = [
            'id',
            'name',
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        read_only_fields = [
            'id',
            'updated_at',
            'created_at',
        ]

        fields = [
            'id',
            'name',
        ]


class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        read_only_fields = [
            'id',
            'updated_at',
            'created_at',
        ]

        fields = ['id', 'name']


class CommentReadSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Comment
        read_only_fields = [
            'id',
            'user',
            'updated_at',
            'created_at',
        ]

        fields = [
            'id',
            'comment',
            'item',
            'user',
        ]


class CommentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        read_only_fields = [
            'id',
            'user',
            'updated_at',
            'created_at',
        ]
        fields = [
            'id',
            'comment',
            'item',
            'user',
        ]


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        read_only_fields = [
            'id',
            'user',
            'updated_at',
            'created_at',
        ]
        fields = [
            'id',
            'item',
            'user'
        ]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:

        model = Image
        read_only_fields = [
            'id',
            'updated_at',
            'created_at',
        ]

        fields = [
            'id',
            'image',
            'item',
        ]


class ItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        read_only_fields = [
            'id',
            'user',
            'updated_at',
            'created_at',
        ]

        fields = [
            'id',
            'user',
            'title',
            'sold',
            'description',
            'year',
            'price',
            'category',
            'brand',
            'condition',
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

        read_only_fields = [
            'id',
            'user',
            'updated_at',
            'created_at',
        ]

        fields = [
            'id',
            'user',
            'title',
            'sold',
            'description',
            'year',
            'price',
            'category',
            'brand',
            'images',
            'likes',
            'comments',
            'condition',
        ]
