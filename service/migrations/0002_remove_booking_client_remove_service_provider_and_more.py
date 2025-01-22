# Generated by Django 5.1.4 on 2025-01-22 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("service", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="booking",
            name="client",
        ),
        migrations.RemoveField(
            model_name="service",
            name="provider",
        ),
        migrations.AddField(
            model_name="booking",
            name="client_id",
            field=models.CharField(default="1", max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="service",
            name="provider_id",
            field=models.CharField(default="1", max_length=255),
            preserve_default=False,
        ),
    ]
