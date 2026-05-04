# Generated manually to restore the initial Django member model migration.

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="GymMember",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("surname", models.CharField(max_length=100)),
                ("tel_no", models.CharField(max_length=20)),
                ("membership_card", models.CharField(max_length=50, unique=True)),
            ],
        ),
    ]
