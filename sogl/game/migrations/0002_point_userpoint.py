# Generated by Django 4.2.13 on 2024-09-06 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("game", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Point",
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
                "db_table": "point",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="UserPoint",
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
                ("point_id", models.BigIntegerField()),
                ("amount", models.BigIntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "user_point",
                "abstract": False,
            },
        ),
    ]
