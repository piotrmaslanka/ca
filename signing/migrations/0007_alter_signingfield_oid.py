# Generated by Django 5.0.7 on 2024-07-17 10:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("signing", "0006_signing_next_serial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="signingfield",
            name="oid",
            field=models.CharField(max_length=255, verbose_name="According to RFC3061"),
        ),
    ]
