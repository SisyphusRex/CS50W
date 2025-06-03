from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django import forms

from decimal import Decimal

from .models import User, Listing, Bid, Comment, Category


class BidForm(forms.Form):
    bid = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.TextInput(attrs={"placeholder": "Bid"}),
        label="",
    )


def index(request):

    active_listings = Listing.objects.filter(is_active=True).order_by("-created_at")

    return render(
        request,
        "auctions/index.html",
        {"active_listings": active_listings},
    )


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def listing(request, listing_id):

    this_listing = Listing.objects.get(pk=listing_id)
    bids = this_listing.bids_by_listing.all()
    number_of_bids = bids.count()
    try:
        current_bid = this_listing.bids_by_listing.get(is_current=True)
    except ObjectDoesNotExist:
        print("No current price.")
    except MultipleObjectsReturned:
        print("More than one current bid.")

    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            bid_amount = form.cleaned_data["bid"]

        else:
            return render(
                request,
                "auctions/listing.html",
                {
                    "listing": this_listing,
                    "bids": bids,
                    "current_bid": current_bid,
                    "number_of_bids": number_of_bids,
                    "bid_form": BidForm(),
                },
            )

        if bid_amount > this_listing.current_price:
            Decimal(bid_amount)
            new_bid = Bid(
                user=request.user,
                listing=this_listing,
                amount=bid_amount,
                is_current=True,
            )
            new_bid.save()
            current_bid.is_current = False
            current_bid.save()
            this_listing.current_price = new_bid.amount
            this_listing.save()

            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

        else:
            return render(
                request,
                "auctions/listing.html",
                {
                    "listing": this_listing,
                    "bids": bids,
                    "current_bid": current_bid,
                    "number_of_bids": number_of_bids,
                    "bid_form": BidForm(),
                },
            )

    return render(
        request,
        "auctions/listing.html",
        {
            "listing": this_listing,
            "bids": bids,
            "current_bid": current_bid,
            "number_of_bids": number_of_bids,
            "bid_form": BidForm(),
        },
    )
