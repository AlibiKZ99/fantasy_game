# Generated by Django 3.2.9 on 2021-12-07 16:39

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Player",
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
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
                ("country", models.CharField(max_length=100)),
                (
                    "age",
                    models.PositiveIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(18),
                            django.core.validators.MaxValueValidator(40),
                        ]
                    ),
                ),
                (
                    "market_value",
                    models.PositiveIntegerField(
                        default=1000000,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "position",
                    models.CharField(
                        choices=[
                            ("Goalkeeper", "Goalkeeper"),
                            ("Defender", "Defender"),
                            ("Midfielder", "Midfielder"),
                            ("Attacker", "Attacker"),
                        ],
                        max_length=20,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Team",
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
                ("country", models.CharField(max_length=100)),
                (
                    "team_money",
                    models.PositiveIntegerField(
                        default=5000000,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Transfer",
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
                ("is_sold", models.BooleanField(default=False)),
                (
                    "asking_price",
                    models.PositiveIntegerField(
                        validators=[django.core.validators.MinValueValidator(1)]
                    ),
                ),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING, to="core.player"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TransferHistory",
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
                ("transferred_time", models.DateField(auto_now_add=True)),
                (
                    "buying_team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="purchases",
                        to="core.team",
                    ),
                ),
                (
                    "selling_team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="sales",
                        to="core.team",
                    ),
                ),
                (
                    "transfer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="core.transfer",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="player",
            name="team",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="players",
                to="core.team",
            ),
        ),
    ]
