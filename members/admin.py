from django.contrib import admin

from members.models import GymMember, PriceItem, ScheduleEntry


@admin.register(GymMember)
class GymMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "surname", "membership_card", "tel_no")
    search_fields = ("name", "surname", "membership_card")


@admin.register(PriceItem)
class PriceItemAdmin(admin.ModelAdmin):
    list_display = ("entry_type", "visits_per_month", "price", "payment_method")
    search_fields = ("entry_type", "price", "payment_method")


@admin.register(ScheduleEntry)
class ScheduleEntryAdmin(admin.ModelAdmin):
    list_display = (
        "time_range",
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    )
    search_fields = (
        "time_range",
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    )
