# Generated by Django 5.2.1 on 2025-06-03 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_listing_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='current_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
