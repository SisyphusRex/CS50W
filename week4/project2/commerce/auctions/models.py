from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """user class"""

    id = models.AutoField(primary_key=True)


class Category(models.Model):
    """listing category class"""

    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=64)


class Listing(models.Model):
    """auction listing class"""

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=500, blank=True)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listings_by_user"
    )
    image_url = models.URLField(max_length=200)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="listings_by_category"
    )


class Bid(models.Model):
    """bid class"""

    id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bids_by_user"
    )
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="bids_by_listing"
    )


class Comment(models.Model):
    """comment class"""

    id = models.AutoField(primary_key=True)
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="listing_comments"
    )
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_comments"
    )
    comment = models.CharField(max_length=500)
