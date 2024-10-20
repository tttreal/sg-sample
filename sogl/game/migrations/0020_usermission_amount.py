# Generated by Django 4.2.16 on 2024-09-20 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("game", "0019_mission_usermission"),
    ]

    operations = [
        migrations.RunSQL(
            sql=[
                """
                ALTER TABLE user_mission ADD COLUMN count int DEFAULT 0 AFTER mission_id;
                """
            ],
            reverse_sql=[
                """
                ALTER TABLE user_mission DROP COLUMN count;
                """
            ],
        ),
        migrations.SeparateDatabaseAndState(
            database_operations=[
            ],
            state_operations=[
                migrations.AddField(
                    model_name="usermission",
                    name="count",
                    field=models.IntegerField(default=0),
                ),
            ]
        )
    ]
