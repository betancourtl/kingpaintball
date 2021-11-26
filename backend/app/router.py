from app.viewsets import UserViewSet

def register_viewset(router):
  router.register(r'users', UserViewSet)