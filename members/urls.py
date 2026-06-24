from django.urls import path

from members import views


app_name = "members"

urlpatterns = [
    path("", views.home, name="home"),
    path("wyloguj/", views.logout_user, name="logout"),
    path("konto/", views.account_details, name="account"),
    path("konto/zmiana-hasla/", views.change_password, name="change_password"),
    path("faq/", views.faq, name="faq"),
    path("kontakt/", views.contact, name="contact"),
    path("cennik/", views.price_list, name="price_list"),
    path("cennik/<int:price_id>/wybierz/", views.select_plan, name="select_plan"),
    path("grafik/", views.schedule, name="schedule"),
    path("members/", views.member_list, name="list"),
    path("members/add/", views.member_create, name="add"),
    path("members/<int:member_id>/edit/", views.member_update, name="edit"),
    path("members/<int:member_id>/delete/", views.member_delete, name="delete"),
]
