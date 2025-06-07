from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """user class"""

    id = models.AutoField(
        primary_key=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )


class Category(models.Model):
    """listing category class"""

    id = models.AutoField(
        primary_key=True,
    )
    title = models.CharField(
        max_length=64,
    )

    def __str__(self):
        return f"{self.title}"


class Listing(models.Model):
    """auction listing class"""

    id = models.AutoField(
        primary_key=True,
    )
    title = models.CharField(
        max_length=64,
    )
    description = models.CharField(
        max_length=500,
        blank=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="listings_by_user",
    )
    image_url = models.URLField(
        max_length=300,
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="listings_by_category",
    )
    is_active = models.BooleanField(
        default=True,
    )
    watchers = models.ManyToManyField(
        User,
        blank=True,
        related_name="watched_listings",
    )
    winner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="won_listings_by_user",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    current_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )

    def __str__(self):
        return f"{self.title}"


class Bid(models.Model):
    """bid class"""

    id = models.AutoField(
        primary_key=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bids_by_user",
    )
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="bids_by_listing",
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    is_current = models.BooleanField(
        default=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.amount}"


class Comment(models.Model):
    """comment class"""

    id = models.AutoField(
        primary_key=True,
    )
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="listing_comments",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_comments",
    )
    comment = models.CharField(
        max_length=500,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.comment}"
