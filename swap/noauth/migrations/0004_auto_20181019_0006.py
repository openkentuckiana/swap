# Generated by Django 2.1.2 on 2018-10-19 00:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("noauth", "0003_user_building")]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="building",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="districts.Building",
            ),
        )
    ]