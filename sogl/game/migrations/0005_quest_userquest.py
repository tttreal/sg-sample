# Generated by Django 4.2.16 on 2024-09-15 04:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("game", "0004_rename_userpartymember_userpartychara_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Quest",
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
                ("power", models.BigIntegerField()),
                ("display_order", models.IntegerField()),
                ("need_stamina", models.IntegerField()),
                ("clear_present_id", models.BigIntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "quest",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="UserQuest",
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
                ("quest_id", models.BigIntegerField()),
                ("is_clear", models.BooleanField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "user_quest",
                "abstract": False,
            },
        ),
    ]
