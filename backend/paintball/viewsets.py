from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import (IsAuthenticatedOrReadOnly, IsAdminUser)
from paintball.permissions import (
    IsReadOnly,
    IsOwnerOrReadOnly,
    IsImageOwnerOrReadOnly
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
User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


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
    filterset_fields = [
        'sold',
        'year',
        'price',
        'category',
        'brand',
        'condition',
    ]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    # POST
    # Will add the user to the object on a post request
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsImageOwnerOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # check user owns the item.
        item_id = request.data.get('item', None)
        item = Item.objects.get(pk=item_id)

        if not item:
            response = {'message': 'Item does not exist'}
            return Response(response, status=status.HTTP_403_FORBIDDEN)

        is_owner = item.user == self.request.user

        if not is_owner:
            response = {'message': 'User does not own the item'}
            return Response(response, status=status.HTTP_403_FORBIDDEN)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, pk=None):
        response = {'message': 'Update function is not offered in this path.'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None):
        response = {'message': 'Update function is not offered in this path.'}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)


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
