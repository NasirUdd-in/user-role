# Generated by Django 4.2.7 on 2023-12-11 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wallets", "0004_customgroup"),
    ]

    operations = [
        migrations.CreateModel(
            name="Product",
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
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("description", models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name="custompermission",
            name="group",
        ),
        migrations.RemoveField(
            model_name="custompermission",
            name="permission",
        ),
        migrations.DeleteModel(
            name="CustomGroup",
        ),
        migrations.DeleteModel(
            name="CustomPermission",
        ),
        migrations.DeleteModel(
            name="PermissionGroup",
        ),
    ]
