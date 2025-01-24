# Generated by Django 5.1.4 on 2025-01-24 12:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("service", "0002_remove_booking_client_remove_service_provider_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="payment",
            name="booking",
        ),
        migrations.AddField(
            model_name="service",
            name="availability_end",
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="service",
            name="availability_start",
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="service",
            name="is_available",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="service",
            name="description",
            field=models.TextField(blank=True, default=1),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name="BlockedTime",
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
                ("start_time", models.DateTimeField()),
                ("end_time", models.DateTimeField()),
                ("reason", models.CharField(blank=True, max_length=255)),
                (
                    "service",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="blocked_times",
                        to="service.service",
                    ),
                ),
            ],
            options={
                "unique_together": {("service", "start_time", "end_time")},
            },
        ),
        migrations.DeleteModel(
            name="Booking",
        ),
        migrations.DeleteModel(
            name="Payment",
        ),
    ]
