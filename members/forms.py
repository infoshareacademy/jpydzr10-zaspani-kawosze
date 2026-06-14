from django import forms

from members.models import GymMember


class GymMemberForm(forms.ModelForm):
    class Meta:
        model = GymMember
        fields = ["name", "surname", "tel_no", "membership_card"]
        labels = {
            "name": "Imie",
            "surname": "Nazwisko",
            "tel_no": "Numer telefonu",
            "membership_card": "Numer karty czlonkowskiej",
        }


class ContactForm(forms.Form):
    name = forms.CharField(label="Imie i nazwisko", max_length=100)
    email = forms.EmailField(label="Adres e-mail")
    message = forms.CharField(label="Wiadomosc", widget=forms.Textarea)
