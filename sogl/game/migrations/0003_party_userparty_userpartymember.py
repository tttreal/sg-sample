# Generated by Django 4.2.16 on 2024-09-11 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("game", "0002_point_userpoint"),
    ]

    operations = [
        migrations.CreateModel(
            name="Party",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "party",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="UserParty",
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
                ("user_id", models.BigIntegerField()),
                ("party_id", models.BigIntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "user_party",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="UserPartyMember",
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
                ("user_party_id", models.BigIntegerField()),
                ("user_chara_id", models.BigIntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "user_party_member",
                "abstract": False,
            },
        ),
    ]
