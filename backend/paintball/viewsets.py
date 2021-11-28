from rest_framework import viewsets
from core.models import User
from rest_framework.permissions import IsAuthenticated
from paintball.mixins import ReadWriteSerializerMixin
from paintball.serializers import (
    BrandSerializer,
    CategorySerializer,
    ConditionSerializer,
    CommentReadSerializer,
    CommentWriteSerializer,
    LikeSerializer,
    ItemReadSerializer,
    ItemWriteSerializer,
    ImageSerializer,
    UserSerializer
)
from paintball.models import (
    Brand,
    Category,
    Comment,
    Condition,
    Like,
    Item,
    Image
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CommentViewSet(ReadWriteSerializerMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    read_serializer_class = CommentReadSerializer
    write_serializer_class = CommentWriteSerializer


class ConditionViewSet(viewsets.ModelViewSet):
    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class ItemViewSet(ReadWriteSerializerMixin, viewsets.ModelViewSet):
    queryset = Item.objects.all()
    read_serializer_class = ItemReadSerializer
    write_serializer_class = ItemWriteSerializer

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
