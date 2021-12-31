from paintball.viewsets import (
    BrandViewSet,
    CategoryViewSet,
    ConditionViewSet,
    CommentViewSet,
    ItemViewSet,
    LikeViewSet,
    ImageViewSet,
)


route_list = (
    (r'brands', BrandViewSet),
    (r'categories', CategoryViewSet),
    (r'conditions', ConditionViewSet),
    (r'comments', CommentViewSet),
    (r'items', ItemViewSet),
    (r'likes', LikeViewSet),
    (r'images', ImageViewSet),
)
