from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("david", views.david, name="david"),
    path("brian", views.brian, name="brian"),
    path(
        "<str:name>", views.greet, name="greet"
    ),  # <str:name> assigns the variable name with string from url and is used in views.py
]
