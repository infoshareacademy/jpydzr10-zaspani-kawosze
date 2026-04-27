from django import forms

from members.models import GymMember


class GymMemberForm(forms.ModelForm):
    class Meta:
        model = GymMember
        fields = ["name", "surname", "tel_no", "membership_card"]
        labels = {
            "name": "Imię",
            "surname": "Nazwisko",
            "tel_no": "Numer telefonu",
            "membership_card": "Numer karty członkowskiej",
        }
