# Generated by Django 2.1.2 on 2018-10-07 14:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("items", "0001_initial")]

    operations = [
        migrations.RemoveField(model_name="itemimage", name="deleted"),
        migrations.AlterField(
            model_name="itemimage",
            name="image",
            field=models.ImageField(
                height_field="height",
                upload_to="uploads/%Y/%m/%d/",
                width_field="width",
            ),
        ),
        migrations.AlterField(
            model_name="itemimage",
            name="item",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="items.Item"
            ),
        ),
    ]