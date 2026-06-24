import calendar

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils import timezone
from django.views.decorators.cache import never_cache

from members.forms import (
    AccountDetailsForm,
    ContactForm,
    GymMemberForm,
    MemberRegistrationForm,
)
from members.models import GymMember, PriceItem, ScheduleEntry


superuser_required = user_passes_test(
    lambda user: user.is_superuser,
    login_url="/admin/login/",
)

def home(request: HttpRequest) -> HttpResponse:
    return render(request, "home.html")


def logout_user(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("members:home")


@login_required(login_url="/admin/login/")
def account_details(request: HttpRequest) -> HttpResponse:
    member, _ = GymMember.objects.get_or_create(
        user=request.user,
        defaults={
            "name": request.user.username,
            "surname": "-",
            "tel_no": "",
        },
    )

    if request.method == "POST":
        form = AccountDetailsForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, "Dane konta zostały pomyślnie zapisane.")
            return redirect("members:account")
    else:
        form = AccountDetailsForm(instance=member)

    return render(
        request,
        "account/details.html",
        {
            "member": member,
            "form": form,
        },
    )


@login_required(login_url="/admin/login/")
def change_password(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Hasło zostało pomyślnie zmienione.")
            return redirect("members:account")
    else:
        form = PasswordChangeForm(request.user)

    return render(
        request,
        "account/change_password.html",
        {"form": form},
    )


def admin_login_or_register(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect("/admin/")
        return redirect("members:home")

    next_url = request.GET.get("next") or request.POST.get("next") or "members:home"
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = "members:home"

    is_register = request.GET.get("register") == "1" or request.POST.get("mode") == "register"

    if request.method == "POST" and is_register:
        register_form = MemberRegistrationForm(request.POST)
        login_form = AuthenticationForm(request=request)

        if register_form.is_valid():
            user = register_form.save()
            for attempt in range(5):
                try:
                    GymMember.objects.create(
                        user=user,
                        name=user.username,
                        surname="-",
                        tel_no="",
                    )
                    break
                except IntegrityError:
                    if attempt == 4:
                        user.delete()
                        raise

            login(request, user)
            return redirect(next_url)
    elif request.method == "POST":
        login_form = AuthenticationForm(request=request, data=request.POST)
        register_form = MemberRegistrationForm()

        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            if user.is_superuser:
                return redirect("/admin/")
            return redirect(next_url)
    else:
        login_form = AuthenticationForm(request=request)
        register_form = MemberRegistrationForm()

    return render(
        request,
        "admin/login.html",
        {
            "form": register_form if is_register else login_form,
            "login_form": login_form,
            "register_form": register_form,
            "is_register": is_register,
            "next": next_url,
            "site_header": "Rejestracja" if is_register else "Logowanie",
            "title": "Rejestracja" if is_register else "Logowanie",
        },
    )


def faq(request: HttpRequest) -> HttpResponse:
    faq_path = settings.BASE_DIR / "Faq.txt"
    questions = _read_text_lines(faq_path)
    faq_sections = _build_faq_sections(questions)

    return render(
        request,
        "faq.html",
        {"faq_sections": faq_sections},
    )


def contact(request):

    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():

            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]
            subject = f"Wiadomość od {name}"
            email_body = f"Email nadawcy: {email}\n\n{message}"
            recipient_list = list(
                get_user_model()
                .objects.filter(is_superuser=True, is_active=True)
                .exclude(email="")
                .values_list("email", flat=True)
                .distinct()
            )

            if recipient_list:
                send_mail(
                    subject=subject,
                    message=email_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=recipient_list,
                )
                messages.success(request, "Wiadomość została wysłana do administratora!")
            else:
                print("\n--- WIADOMOŚĆ Z FORMULARZA KONTAKTOWEGO ---")
                print(f"Temat: {subject}")
                print(email_body)
                print("--- BRAK SUPERUSERA Z ADRESEM E-MAIL ---\n")
                messages.success(
                    request,
                    "Brak adresu administratora. Wiadomość została zapisana w konsoli.",
                )
            return redirect("members:contact")

    else:
        form = ContactForm()

    return render(request, "contact.html", {
        "form": form
    })


def price_list(request: HttpRequest) -> HttpResponse:
    prices = PriceItem.objects.filter(is_active=True)

    return render(
        request,
        "price_list.html",
        {"prices": prices},
    )


@login_required(login_url="/admin/login/")
def select_plan(request: HttpRequest, price_id: int) -> HttpResponse:
    price = get_object_or_404(PriceItem, pk=price_id, is_active=True)

    if request.method == "POST":
        purchased_at = timezone.now()
        member, _ = GymMember.objects.get_or_create(
            user=request.user,
            defaults={
                "name": request.user.username,
                "surname": "-",
                "tel_no": "",
            },
        )
        member.membership_plan = price
        member.membership_started_at = purchased_at
        member.membership_expires_at = _add_months(
            purchased_at,
            price.duration_months,
        )
        member.save(
            update_fields=[
                "membership_plan",
                "membership_started_at",
                "membership_expires_at",
            ]
        )
        messages.success(
            request,
            f"Karnet {price.display_name} został aktywowany.",
        )
        return redirect("members:price_list")

    return render(
        request,
        "payment_simulation.html",
        {"price": price},
    )


def schedule(request: HttpRequest) -> HttpResponse:
    entries = ScheduleEntry.objects.all()

    return render(
        request,
        "schedule.html",
        {"entries": entries},
    )


@never_cache
@superuser_required
def member_list(request: HttpRequest) -> HttpResponse:
    members = GymMember.objects.all().order_by("surname", "name")
    return render(
        request,
        "members/member_list.html",
        {"members": members},
    )


@never_cache
@superuser_required
def member_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = GymMemberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Klubowicz został pomyślnie dodany.")
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


@never_cache
@superuser_required
def member_update(request: HttpRequest, member_id: int) -> HttpResponse:
    member = get_object_or_404(GymMember, pk=member_id)

    if request.method == "POST":
        form = GymMemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, "Dane klubowicza zostały pomyślnie zaktualizowane.")
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


@never_cache
@superuser_required
def member_delete(request: HttpRequest, member_id: int) -> HttpResponse:
    member = get_object_or_404(GymMember, pk=member_id)

    if request.method == "POST":
        member.delete()
        messages.success(request, "Klubowicz został pomyślnie usunięty.")
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


def _build_faq_sections(lines):
    sections = []
    current_section = {"title": "Najczęstsze pytania", "items": []}

    for line in lines:
        if line.startswith("### "):
            if current_section["items"]:
                sections.append(current_section)
            current_section = {"title": line.replace("### ", "", 1), "items": []}
            continue

        if line.startswith("P: "):
            current_section["items"].append(
                {
                    "question": line.replace("P: ", "", 1),
                    "answer": "",
                }
            )
            continue

        if line.startswith("O: ") and current_section["items"]:
            current_section["items"][-1]["answer"] = line.replace("O: ", "", 1)

    if current_section["items"]:
        sections.append(current_section)

    return sections


def _add_months(value, months):
    month_index = value.month - 1 + months
    year = value.year + month_index // 12
    month = month_index % 12 + 1
    day = min(value.day, calendar.monthrange(year, month)[1])
    return value.replace(year=year, month=month, day=day)
