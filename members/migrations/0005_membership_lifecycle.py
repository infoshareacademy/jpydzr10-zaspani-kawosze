import re
import secrets

import django.db.models.deletion
import members.models
from django.db import migrations, models


HEX_CARD_PATTERN = re.compile(r"^[0-9A-F]{6}$")


def prepare_membership_data(apps, schema_editor):
    GymMember = apps.get_model("members", "GymMember")
    PriceItem = apps.get_model("members", "PriceItem")

    durations = (1, 3, 6)
    for index, plan in enumerate(PriceItem.objects.order_by("id")):
        plan.duration_months = durations[index] if index < len(durations) else 1
        plan.is_active = index < len(durations)
        plan.save(update_fields=["duration_months", "is_active"])

    members = list(GymMember.objects.order_by("id"))
    reserved_cards = {
        (member.membership_card or "").upper()
        for member in members
        if HEX_CARD_PATTERN.fullmatch((member.membership_card or "").upper())
    }
    used_cards = set()
    for member in members:
        current_card = (member.membership_card or "").upper()
        if HEX_CARD_PATTERN.fullmatch(current_card) and current_card not in used_cards:
            used_cards.add(current_card)
            continue

        new_card = secrets.token_hex(3).upper()
        while new_card in reserved_cards or new_card in used_cards:
            new_card = secrets.token_hex(3).upper()

        member.membership_card = new_card
        member.save(update_fields=["membership_card"])
        used_cards.add(new_card)
        reserved_cards.add(new_card)


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0004_priceitem_is_active"),
    ]

    operations = [
        migrations.AddField(
            model_name="gymmember",
            name="membership_expires_at",
            field=models.DateTimeField(
                blank=True,
                null=True,
                verbose_name="Data wygasniecia karnetu",
            ),
        ),
        migrations.AddField(
            model_name="gymmember",
            name="membership_plan",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="members",
                to="members.priceitem",
                verbose_name="Zakupiony karnet",
            ),
        ),
        migrations.AddField(
            model_name="gymmember",
            name="membership_started_at",
            field=models.DateTimeField(
                blank=True,
                null=True,
                verbose_name="Data zakupu karnetu",
            ),
        ),
        migrations.AddField(
            model_name="priceitem",
            name="duration_months",
            field=models.PositiveSmallIntegerField(
                choices=[(1, "1 miesiac"), (3, "3 miesiace"), (6, "6 miesiecy")],
                null=True,
                verbose_name="Okres karnetu",
            ),
        ),
        migrations.RunPython(prepare_membership_data, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="priceitem",
            name="visits_per_month",
        ),
        migrations.AlterField(
            model_name="priceitem",
            name="duration_months",
            field=models.PositiveSmallIntegerField(
                choices=[(1, "1 miesiac"), (3, "3 miesiace"), (6, "6 miesiecy")],
                verbose_name="Okres karnetu",
            ),
        ),
        migrations.AlterField(
            model_name="gymmember",
            name="membership_card",
            field=models.CharField(
                db_column="membershipcard",
                default=members.models.generate_membership_card,
                editable=False,
                max_length=6,
                unique=True,
                verbose_name="Numer karty",
            ),
        ),
    ]
