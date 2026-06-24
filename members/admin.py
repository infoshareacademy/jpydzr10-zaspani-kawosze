from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone

from members.models import GymMember, PriceItem, ScheduleEntry
from members.reports import build_members_pdf


@admin.action(description="Pobierz raport wybranych klubowiczów (PDF)")
def export_members_pdf(modeladmin, request, queryset):
    pdf_content = build_members_pdf(queryset)
    filename = timezone.localtime().strftime("raport_klubowiczow_%Y%m%d_%H%M.pdf")
    response = HttpResponse(pdf_content, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


@admin.register(GymMember)
class GymMemberAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "surname",
        "membership_card",
        "tel_no",
        "user",
        "membership_plan",
        "membership_expires_at",
    )
    search_fields = ("name", "surname", "membership_card", "user__username")
    list_filter = ("membership_plan",)
    actions = (export_members_pdf,)


@admin.register(PriceItem)
class PriceItemAdmin(admin.ModelAdmin):
    list_display = (
        "entry_type",
        "duration_months",
        "price",
        "payment_method",
        "is_active",
    )
    list_filter = ("is_active",)
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
