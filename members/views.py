from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from members.forms import GymMemberForm
from members.models import GymMember, PriceItem, ScheduleEntry


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "home.html")


def faq(request: HttpRequest) -> HttpResponse:
    faq_path = settings.BASE_DIR / "Faq.txt"
    questions = _read_text_lines(faq_path)

    return render(
        request,
        "faq.html",
        {"questions": questions},
    )


def contact(request: HttpRequest) -> HttpResponse:
    contact_path = settings.BASE_DIR / "Kontakt.txt"
    contact_lines = _read_text_lines(contact_path)

    return render(
        request,
        "contact.html",
        {"contact_lines": contact_lines},
    )


def price_list(request: HttpRequest) -> HttpResponse:
    prices = PriceItem.objects.all()

    return render(
        request,
        "price_list.html",
        {"prices": prices},
    )


def schedule(request: HttpRequest) -> HttpResponse:
    entries = ScheduleEntry.objects.all()

    return render(
        request,
        "schedule.html",
        {"entries": entries},
    )


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


def _read_text_lines(file_path):
    if not file_path.exists():
        return []

    return [
        line.strip()
        for line in file_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
