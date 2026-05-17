from django.urls import path

from members import views


app_name = "members"

urlpatterns = [
    path("", views.home, name="home"),
    path("faq/", views.faq, name="faq"),
    path("kontakt/", views.contact, name="contact"),
    path("cennik/", views.price_list, name="price_list"),
    path("grafik/", views.schedule, name="schedule"),
    path("members/", views.member_list, name="list"),
    path("members/add/", views.member_create, name="add"),
    path("members/<int:member_id>/edit/", views.member_update, name="edit"),
    path("members/<int:member_id>/delete/", views.member_delete, name="delete"),
]
