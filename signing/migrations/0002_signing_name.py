# Generated by Django 5.0.7 on 2024-07-16 17:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("signing", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="signing",
            name="name",
            field=models.CharField(default="default", max_length=200),
            preserve_default=False,
        ),
    ]
