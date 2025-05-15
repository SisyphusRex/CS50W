# System Imports

# Third Party Imports
from django.urls import path

# First Party Imports
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("<int:flight_id>", views.flight, name="flight"),
]
