from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django import forms
from django.forms import ModelForm, Textarea, DecimalField, TextInput

from decimal import Decimal

from .models import User, Listing, Bid, Comment, Category


class BidForm(forms.Form):
    bid = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.TextInput(attrs={"placeholder": "Bid"}),
        label="",
    )


class CreateForm(forms.Form):
    title = forms.CharField(
        max_length=64,
        widget=forms.TextInput(attrs={"placeholder": "Title"}),
        label="Title*",
    )
    description = forms.CharField(
        max_length=500,
        widget=forms.TextInput(attrs={"placeholder": "Description"}),
        label="Description",
        required=False,
    )
    image_url = forms.URLField(
        max_length=300,
        widget=forms.TextInput(attrs={"placeholder": "Image URL"}),
        label="Image URL",
        required=False,
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label="Category",
        required=False,
    )
    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.TextInput(attrs={"placeholder": "Price"}),
        label="Starting Price*",
    )


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "image_url", "category", "current_price"]
        widgets = {
            "current_price": TextInput(),
            "description": Textarea(),
        }
        labels = {
            "title": "Title",
        }


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
    watchers = this_listing.watchers.all()
    category = this_listing.category
    try:
        current_bid = this_listing.bids_by_listing.get(is_current=True)
    except ObjectDoesNotExist:
        print("No current price.")
    except MultipleObjectsReturned:
        print("More than one current bid.")

    if request.method == "POST":
        # TODO: the view is not creating a new bid when the user submits
        if "bid" in request.POST:
            form = BidForm(request.POST)
            if form.is_valid():
                bid_amount = form.cleaned_data["bid"]
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
                            "watchers": watchers,
                            "category": category,
                        },
                    )
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
                        "watchers": watchers,
                        "category": category,
                    },
                )

        elif "watch" in request.POST:
            this_listing.watchers.add(request.user)
            this_listing.save()
            return render(
                request,
                "auctions/listing.html",
                {
                    "listing": this_listing,
                    "bids": bids,
                    "current_bid": current_bid,
                    "number_of_bids": number_of_bids,
                    "bid_form": BidForm(),
                    "watchers": watchers,
                    "category": category,
                },
            )
        elif "unwatch" in request.POST:
            this_listing.watchers.remove(request.user)
            this_listing.save()
            return render(
                request,
                "auctions/listing.html",
                {
                    "listing": this_listing,
                    "bids": bids,
                    "current_bid": current_bid,
                    "number_of_bids": number_of_bids,
                    "bid_form": BidForm(),
                    "watchers": watchers,
                    "category": category,
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
            "watchers": watchers,
            "category": category,
        },
    )


def categories(request):

    my_categories = Category.objects.all().order_by("title")

    return render(
        request,
        "auctions/categories.html",
        {
            "categories": my_categories,
        },
    )


def category(request, category_id):

    this_category = Category.objects.get(pk=category_id)
    listings_in_category = this_category.listings_by_category.filter(is_active=True)
    return render(
        request,
        "auctions/category.html",
        {
            "listings_in_category": listings_in_category,
            "category": this_category,
        },
    )


@login_required
def watchlist(request):
    user = request.user
    watched_listings = user.watched_listings.all()
    return render(
        request,
        "auctions/watchlist.html",
        {
            "watchlist": watched_listings,
        },
    )


@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            image_url = form.cleaned_data["image_url"]
            category = form.cleaned_data["category"]
            price = form.cleaned_data["current_price"]

            new_listing = Listing(
                title=title,
                description=description,
                image_url=image_url,
                category=category,
                current_price=price,
                user=request.user,
            )
            new_listing.save()
            new_bid = Bid(
                user=request.user,
                listing=new_listing,
                amount=price,
                is_current=True,
            )
            new_bid.save()

            return HttpResponseRedirect(reverse("listing", args=(new_listing.id,)))

        else:
            return render(
                request,
                "auctions/create.html",
                {
                    "create_form": ListingForm(),
                },
            )

    return render(
        request,
        "auctions/create.html",
        {
            "create_form": ListingForm(),
        },
    )
