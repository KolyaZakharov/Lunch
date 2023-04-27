from django.contrib.auth.models import AbstractUser
from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)
    date = models.DateField()
    cuisine = models.CharField(max_length=50)
    items = models.TextField()
    price = models.DecimalField(
        blank=True,
        null=True,
        max_digits=6,
        decimal_places=2
    )

    unique_together = ["restaurant", "date"]

    def __str__(self):
        return f"{self.cuisine} from {self.restaurant}"


class Employee(AbstractUser):
    pass


class Vote(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.PROTECT)
    user = models.ForeignKey(Employee, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.user} on {self.menu}"


class Winner(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.PROTECT)
    vote_count = models.PositiveIntegerField()
    date = models.DateField(editable=False)

    def __str__(self):
        return f"{self.menu} on {self.date}"
