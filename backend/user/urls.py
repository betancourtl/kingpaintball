from user.viewsets import (
    UserViewset,
    SessionViewset,
    AccountViewset,
    VerificationTokenViewset,
)

route_list = (
    (r'users', UserViewset),
    (r'sessions', SessionViewset),
    (r'accounts', AccountViewset),
    (r'verification-tokens', VerificationTokenViewset),
)
