from rest_framework import routers

from user.urls import route_list as user_route_list
from paintball.urls import route_list as paintball_route_list

routeLists = [
    paintball_route_list,
    user_route_list,
]

router = routers.DefaultRouter()

for x in routeLists:
    for route in x:
        router.register(route[0], route[1])
