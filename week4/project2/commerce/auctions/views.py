from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django import forms
from django.forms import ModelForm, Textarea, DecimalField, TextInput
from django.contrib import messages
from django.db.models import Subquery, OuterRef

from decimal import Decimal

from .models import User, Listing, Bid, Comment, Category


# class BidForm(forms.Form):
#     bid = forms.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         label="",
#     )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]
        widgets = {
            "comment": Textarea(),
        }


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["amount"]
        widgets = {
            "amount": TextInput(),
        }


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
            messages.add_message(request, messages.SUCCESS, "Logged In")
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
    messages.add_message(request, messages.SUCCESS, "Logged Out")
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

    def return_redirect():
        return HttpResponseRedirect(
            reverse(
                "listing",
                args=(listing_id,),
            )
        )

    def return_render():
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
                "comments": comments,
                "comment_form": CommentForm(),
            },
        )

    this_listing = Listing.objects.get(pk=listing_id)
    bids = this_listing.bids_by_listing.all()
    number_of_bids = bids.count()
    watchers = this_listing.watchers.all()
    category = this_listing.category
    current_bid = this_listing.bids_by_listing.get(is_current=True)
    comments = this_listing.listing_comments.all()

    if request.method == "POST" and "bid" in request.POST:
        bid_form = BidForm(request.POST)
        if bid_form.is_valid():
            bid_amount = bid_form.cleaned_data["amount"]
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
                this_listing.current_price = bid_amount
                this_listing.save()
                messages.add_message(request, messages.SUCCESS, "Successful Bid")

                return return_redirect()

            else:
                messages.add_message(request, messages.ERROR, "Bid too low")
                return return_render()
        else:
            messages.add_message(request, messages.ERROR, "Invalid input")
            error_dict = bid_form.errors
            bid_errors = error_dict["amount"]
            return return_render()

    if request.method == "POST" and "watch" in request.POST:
        this_listing.watchers.add(request.user)
        this_listing.save()
        return return_redirect()

    if request.method == "POST" and "unwatch" in request.POST:
        this_listing.watchers.remove(request.user)
        this_listing.save()
        return return_redirect()

    if request.method == "POST" and "comment_submit" in request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.cleaned_data["comment"]
            new_comment = Comment(
                listing=this_listing, user=request.user, comment=comment
            )
            new_comment.save()
            messages.add_message(request, messages.SUCCESS, "Comment Added")
            return return_redirect()
        else:
            messages.add_message(request, messages.ERROR, "Invalid input")
            return return_render()

    # TODO: I need to make a function that allows the creator of a listing to close it
    # and then it updates whomever has the highest bid

    if request.method == "POST" and "end" in request.POST:
        this_listing.is_active = False
        this_listing.winner = current_bid.user
        this_listing.save()
        return return_redirect()
    return return_render()


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


def user(request, user_id):
    this_user = User.objects.get(id=user_id)
    watched_listings = this_user.watched_listings.all()
    won_listings = this_user.won_listings_by_user.all()
    created_listings = this_user.listings_by_user.all()
    all_user_bids = this_user.bids_by_user.all()

    active_listings = Listing.objects.filter(is_active=True)

    subquery_user_bids = (
        this_user.bids_by_user.filter(listing=OuterRef("listing"))
        .order_by("-created_at")
        .values("pk")[:1]
    )
    user_bids = this_user.bids_by_user.filter(
        pk__in=Subquery(subquery_user_bids)
    ).order_by("listing", "-created_at")

    active_listing_bids = []
    for bid in user_bids:
        if bid.listing in active_listings:
            active_listing_bids.append(bid)

    return render(
        request,
        "auctions/user.html",
        {
            "user": this_user,
            "watched_listings": watched_listings,
            "won_listings": won_listings,
            "created_listings": created_listings,
            "active_listing_bids": active_listing_bids,
            "all_user_bids": all_user_bids,
        },
    )
