# Generated by Django 5.2.1 on 2025-06-04 22:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_listing_current_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='category',
            new_name='title',
        ),
    ]
