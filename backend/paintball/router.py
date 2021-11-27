from paintball.viewsets import (
  BrandViewSet,
  CategoryViewSet,
  ConditionViewSet,
  CommentViewSet,
  ItemViewSet,
  LikeViewSet,
  ImageViewSet,
  UserViewSet
)
def register_viewset(router):
  router.register(r'brands', BrandViewSet)
  router.register(r'categories', CategoryViewSet)
  router.register(r'conditions', ConditionViewSet)
  router.register(r'comments', CommentViewSet)
  router.register(r'items', ItemViewSet)
  router.register(r'likes', LikeViewSet)
  router.register(r'images', ImageViewSet)
  router.register(r'users', UserViewSet)
