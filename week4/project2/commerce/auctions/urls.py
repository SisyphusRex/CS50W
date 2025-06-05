from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listings/<int:listing_id>", views.listing, name="listing"),
    path("create", views.create_listing, name="create"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:category_id>", views.category, name="category"),
]
