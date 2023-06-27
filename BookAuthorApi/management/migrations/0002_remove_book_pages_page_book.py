# Generated by Django 4.2.2 on 2023-06-24 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("management", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="book",
            name="pages",
        ),
        migrations.AddField(
            model_name="page",
            name="book",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="page",
                to="management.book",
            ),
            preserve_default=False,
        ),
    ]