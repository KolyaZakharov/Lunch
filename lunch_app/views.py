from datetime import datetime

from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from lunch_app.models import Restaurant, Menu, Employee, Vote, Winner
from lunch_app.permissions import IsAdminUserOrReadOnly
from lunch_app.serializers import (
    RestaurantSerializer,
    EmployeeSerializer,
    MenuSerializer,
    VoteSerializer,
    WinnerSerializer,
)


class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAdminUser]


class MenuViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUserOrReadOnly]
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class EmployeeViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class VoteViewSet(ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def get_queryset(self):
        return Vote.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WinnerViewSet(ModelViewSet):
    queryset = Winner.objects.all()
    serializer_class = WinnerSerializer

    def perform_create(self, instance):
        instance.save(date=datetime.today().date())
