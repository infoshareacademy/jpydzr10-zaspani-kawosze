from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0003_gymmember_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="priceitem",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="Aktywny plan"),
        ),
    ]
