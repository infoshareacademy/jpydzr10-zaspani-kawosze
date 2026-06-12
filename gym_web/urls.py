"""
URL configuration for gym_web project.
"""

from django.contrib import admin
from django.contrib.auth.forms import AuthenticationForm
from django.urls import include, path

from members.views import admin_login_or_register


admin.site.login_form = AuthenticationForm
admin.site.site_header = "Administracja Django"
admin.site.site_title = "Administracja Django"
admin.site.index_title = "Panel administratora"

urlpatterns = [
    path("admin/login/", admin_login_or_register, name="admin_login"),
    path("admin/", admin.site.urls),
    path("", include("members.urls")),
]
