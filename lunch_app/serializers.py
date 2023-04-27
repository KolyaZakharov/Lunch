from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db.models import Count
from rest_framework import serializers

from lunch_app.models import Restaurant, Menu, Employee, Vote, Winner


def get_last_n_working_days(n):
    last_working_days = []
    delta = 1
    today = datetime.today().date()

    while len(last_working_days) < n:
        day = today - timedelta(days=delta)
        delta += 1
        if day.weekday() < 5:
            last_working_days.append(day)
    return last_working_days


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"


class EmployeeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={"input_type": "password"},
        write_only=True
    )

    class Meta:
        model = Employee
        fields = [
            "id",
            "username",
            "password",
            "is_active",
            "is_staff",
            "is_superuser"
        ]
        read_only_fields = ("id", "is_staff")
        extra_kwargs = {"password": {"write_only": True, "min_length": 6}}

    def create(self, validated_data):
        """Create employee with encrypted password"""
        return get_user_model().object.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update employee with  correctly encrypted password"""
        password = validated_data.pop("password", None)
        employee = super().update(instance, validated_data)

        if password:
            employee.set_password(password)
            employee.save()

        return employee

    @staticmethod
    def validate_password(password):
        validate_password(password)
        return password


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = "__all__"


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = "__all__"

    def validate(self, data):
        user = self.context["request"].user
        menu = data["menu"]

        if menu.date < datetime.today().date():
            raise serializers.ValidationError(
                "User cannot vote for past dates!"
            )

        already_voted = Vote.objects.filter(user=user, menu__date=menu.date)
        if already_voted:
            raise serializers.ValidationError("User has already voted!")

        voting_concluded = Winner.objects.filter(
            menu__date=datetime.today().date()
        )
        if voting_concluded:
            raise serializers.ValidationError("Voting concluded for the day!")

        recurring_wins = Winner.objects.filter(
            menu__restaurant=menu.restaurant,
            date__in=get_last_n_working_days(2)
        ).count()
        if recurring_wins == 2:
            raise serializers.ValidationError(
                "This restaurant won on last 2 days."
                " Cannot vote for this restaurant!"
            )
        return data


class WinnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Winner
        fields = "__all__"

    def validate(self, data):
        today = datetime.today().date()
        winner_exists = Winner.objects.filter(date=today)
        if winner_exists:
            raise serializers.ValidationError("Winner already exists!")
        return data

    def get_twice_recurring_winner(self):
        return (
            Winner.objects.filter(
                date__in=get_last_n_working_days(2),
                menu__restaurant__in=self.get_last_winner(),
            )
            .values("menu__restaurant")
            .annotate(wins=Count("menu__restaurant"))
            .filter(wins=2)
            .values_list("menu__restaurant", flat=True)
        )

    def get_winning_restaurant(self):
        today = datetime.today().date()
        return (
            Vote.objects.exclude(
                menu__restaurant_id__in=self.get_twice_recurring_winner(),
            )
            .filter(menu__date=today)
            .values(
                "menu_id",
            )
            .annotate(vote_count=Count("menu_id"))
            .latest("vote_count")
        )

    def create(self, validated_data):
        try:
            winner_data = self.get_winning_restaurant()
        except Vote.DoesNotExist:
            raise serializers.ValidationError("Cannot generate a winner!")
        validated_data["menu_id"] = winner_data["menu_id"]
        validated_data["vote_count"] = winner_data["vote_count"]
        return Winner.objects.create(**validated_data)

    @staticmethod
    def get_last_winner():
        return Winner.objects.filter(
            date__in=get_last_n_working_days(1)).values_list(
            "menu__restaurant", flat=True
        )
