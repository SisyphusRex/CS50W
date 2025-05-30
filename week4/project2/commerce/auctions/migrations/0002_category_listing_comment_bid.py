# Generated by Django 5.2.1 on 2025-05-29 20:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('category', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64)),
                ('description', models.CharField(blank=True, max_length=500)),
                ('starting_bid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('current_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image_url', models.URLField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings_by_category', to='auctions.category')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings_by_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('comment', models.CharField(max_length=500)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comments', to=settings.AUTH_USER_MODEL)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listing_comments', to='auctions.listing')),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bids_by_user', to=settings.AUTH_USER_MODEL)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bids_by_listing', to='auctions.listing')),
            ],
        ),
    ]
