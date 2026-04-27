from django.contrib import admin

from members.models import GymMember


@admin.register(GymMember)
class GymMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "surname", "membership_card", "tel_no")
    search_fields = ("name", "surname", "membership_card")

# Register your models here.
