# Generated by Django 5.0.7 on 2024-07-16 18:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("certificates", "0006_certificate_is_used_for_client_auth_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="certificate",
            name="is_used_for_client_auth",
            field=models.BooleanField(
                default=False,
                verbose_name="Can this certificate be used for signing certificates that are meant to be used as client authentication?",
            ),
        ),
    ]
