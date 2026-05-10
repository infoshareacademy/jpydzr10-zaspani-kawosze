from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from members.forms import GymMemberForm
from members.models import GymMember


def home(request: HttpRequest) -> HttpResponse:
    return redirect("members:list")


def member_list(request: HttpRequest) -> HttpResponse:
    members = GymMember.objects.all().order_by("surname", "name")
    return render(
        request,
        "members/member_list.html",
        {"members": members},
    )


def member_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = GymMemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("members:list")
    else:
        form = GymMemberForm()

    return render(
        request,
        "members/member_form.html",
        {
            "form": form,
            "page_title": "Dodaj klubowicza",
            "button_label": "Zapisz",
        },
    )


def member_update(request: HttpRequest, member_id: int) -> HttpResponse:
    member = get_object_or_404(GymMember, pk=member_id)

    if request.method == "POST":
        form = GymMemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect("members:list")
    else:
        form = GymMemberForm(instance=member)

    return render(
        request,
        "members/member_form.html",
        {
            "form": form,
            "page_title": "Edytuj klubowicza",
            "button_label": "Zapisz zmiany",
        },
    )


def member_delete(request: HttpRequest, member_id: int) -> HttpResponse:
    member = get_object_or_404(GymMember, pk=member_id)

    if request.method == "POST":
        member.delete()
        return redirect("members:list")

    return render(
        request,
        "members/member_confirm_delete.html",
        {"member": member},
    )

# Create your views here.
