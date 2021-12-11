from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import (IsAuthenticatedOrReadOnly, IsAdminUser)
from paintball.permissions import (
    IsReadOnly,
    IsOwnerOrReadOnly,
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


def with_user(request: dict) -> dict:
    return {
        **request.data,
        **{'user': request.user.id}
    }


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAdminUser | IsReadOnly]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser | IsReadOnly]


class ConditionViewSet(viewsets.ModelViewSet):
    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer
    permission_classes = [IsAdminUser | IsReadOnly]


class ItemViewSet(ReadWriteSerializerMixin, viewsets.ModelViewSet):
    queryset = Item.objects.all()
    read_serializer_class = ItemReadSerializer
    write_serializer_class = ItemWriteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    # POST
    # Will add the user to the object on a post request
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentViewSet(ReadWriteSerializerMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    read_serializer_class = CommentReadSerializer
    write_serializer_class = CommentWriteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, pk=None):
        response = {'message': 'Update function is not offered in this path.'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None):
        response = {'message': 'Update function is not offered in this path.'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)
