from django import forms
from django.contrib.auth.forms import UserCreationForm

from members.models import GymMember


class GymMemberForm(forms.ModelForm):
    class Meta:
        model = GymMember
        fields = ["name", "surname", "tel_no"]
        labels = {
            "name": "Imię",
            "surname": "Nazwisko",
            "tel_no": "Numer telefonu",
        }


class AccountDetailsForm(forms.ModelForm):
    class Meta:
        model = GymMember
        fields = ["name", "surname", "tel_no"]
        labels = {
            "name": "Imię",
            "surname": "Nazwisko",
            "tel_no": "Numer telefonu",
        }

class ContactForm(forms.Form):
    name = forms.CharField(label="Imię i nazwisko", max_length=100)
    email = forms.EmailField(label="Adres e-mail")
    message = forms.CharField(label="Wiadomość", widget=forms.Textarea)


class MemberRegistrationForm(UserCreationForm):
    username = forms.CharField(label="Login")
    password1 = forms.CharField(label="Hasło", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Powtórz hasło", widget=forms.PasswordInput)
