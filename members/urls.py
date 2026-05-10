from django.urls import path

from members import views


app_name = "members"

urlpatterns = [
    path("", views.home, name="home"),
    path("members/", views.member_list, name="list"),
    path("members/add/", views.member_create, name="add"),
    path("members/<int:member_id>/edit/", views.member_update, name="edit"),
    path("members/<int:member_id>/delete/", views.member_delete, name="delete"),
]
