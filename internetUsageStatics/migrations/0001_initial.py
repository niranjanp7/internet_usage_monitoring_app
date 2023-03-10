# Generated by Django 4.1.5 on 2023-01-26 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DataUsage",
            fields=[
                (
                    "username",
                    models.CharField(max_length=50, primary_key=True, serialize=False),
                ),
                ("mac_address", models.CharField(max_length=17, unique=True)),
                ("start_time", models.DateTimeField()),
                ("usage_time", models.TimeField()),
                ("upload", models.FloatField(default=0)),
                ("download", models.FloatField(default=0)),
            ],
        ),
    ]
