from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from lunch_app.models import Restaurant, Employee, Menu, Vote, Winner


class RestaurantAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = (
        "id",
        "name",
    )
    ordering = ("-id",)


class MenuAdmin(admin.ModelAdmin):
    search_fields = ("cuisine",)
    list_display = (
        "id",
        "date",
        "cuisine",
        "restaurant",
    )
    ordering = ("-id",)


class VoteAdmin(admin.ModelAdmin):
    list_display = ("id", "get_date", "menu", "user")
    ordering = ("-id",)
    readonly_fields = ("get_date",)

    def get_date(self, obj):
        return obj.menu.date

    get_date.short_description = "Date"
    get_date.admin_order_field = "menu__date"


class WinnerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "date",
        "menu",
        "vote_count",
    )
    ordering = ("-id",)
    readonly_fields = ("date",)


admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Employee, UserAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(Winner, WinnerAdmin)
