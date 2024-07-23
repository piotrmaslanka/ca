# Generated by Django 5.0.7 on 2024-07-17 14:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("certificates", "0011_alter_certificate_unique_together"),
        ("signing", "0007_alter_signingfield_oid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="signing",
            name="certificate",
            field=models.ForeignKey(
                help_text="Certificate that will serve as a signer",
                on_delete=django.db.models.deletion.RESTRICT,
                to="certificates.certificate",
                unique=True,
            ),
        ),
    ]
