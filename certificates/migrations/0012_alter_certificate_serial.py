# Generated by Django 5.0.7 on 2024-07-17 15:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("certificates", "0011_alter_certificate_unique_together"),
    ]

    operations = [
        migrations.AlterField(
            model_name="certificate",
            name="serial",
            field=models.CharField(max_length=16),
        ),
    ]
