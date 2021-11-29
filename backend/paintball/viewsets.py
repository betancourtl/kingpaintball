from django.contrib.auth.models import User
from rest_framework import viewsets
from paintball.permissions import (
    IsAdmin,
    IsReadOnly,
    IsOwner,

)
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
    permission_classes = [IsAdmin | IsReadOnly]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdmin | IsReadOnly]


class ConditionViewSet(viewsets.ModelViewSet):
    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer
    permission_classes = [IsAdmin | IsReadOnly]


class ItemViewSet(ReadWriteSerializerMixin, viewsets.ModelViewSet):
    queryset = Item.objects.all()
    read_serializer_class = ItemReadSerializer
    write_serializer_class = ItemWriteSerializer
    permission_classes = [IsAdmin | IsOwner | IsReadOnly]


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAdmin | IsReadOnly]


class CommentViewSet(ReadWriteSerializerMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    read_serializer_class = CommentReadSerializer
    write_serializer_class = CommentWriteSerializer
    permission_classes = [IsAdmin | IsOwner | IsReadOnly]


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAdmin | IsOwner | IsReadOnly]
