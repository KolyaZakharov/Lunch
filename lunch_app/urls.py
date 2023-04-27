from django.urls import path, include
from rest_framework import routers

from lunch_app.views import (
    RestaurantViewSet,
    MenuViewSet,
    EmployeeViewSet,
    VoteViewSet,
    WinnerViewSet,
)

router = routers.DefaultRouter()
router.register("restaurants", RestaurantViewSet)
router.register("menus", MenuViewSet)
router.register("employees", EmployeeViewSet)
router.register("votes", VoteViewSet)
router.register("winners", WinnerViewSet)


urlpatterns = [path("", include(router.urls))]

app_name = "lunch_app"
