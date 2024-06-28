# Generated by Django 5.0.6 on 2024-06-24 18:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("updownfunks", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="file",
            name="folder",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="updownfunks.folder",
            ),
        ),
    ]
