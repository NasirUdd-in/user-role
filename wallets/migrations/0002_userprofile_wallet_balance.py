# Generated by Django 4.2.7 on 2023-11-25 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wallets", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="wallet_balance",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]