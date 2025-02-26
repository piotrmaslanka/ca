# Generated by Django 5.0.7 on 2024-07-16 17:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("certificates", "0004_certificate_kind"),
    ]

    operations = [
        migrations.CreateModel(
            name="Signing",
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
                (
                    "openssl_conf",
                    models.TextField(verbose_name="OpenSSL configuration file"),
                ),
                (
                    "ca",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="certificates.certificate",
                    ),
                ),
            ],
        ),
    ]
