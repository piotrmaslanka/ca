# Generated by Django 5.0.7 on 2024-07-16 17:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("signing", "0003_alter_signing_openssl_conf_signaturedatabase"),
    ]

    operations = [
        migrations.AlterField(
            model_name="signaturedatabase",
            name="revocation",
            field=models.CharField(blank=True, default="", max_length=20),
        ),
        migrations.CreateModel(
            name="SigningField",
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
                ("name", models.CharField(max_length=255)),
                ("oid", models.CharField(max_length=255)),
                ("type", models.CharField(max_length=255)),
                (
                    "signing",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="signing.signing",
                    ),
                ),
            ],
        ),
    ]
