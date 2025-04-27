from django.urls import path
from . import views

app_name = "newyear"
urlpatterns = [
    path("", views.index, name="index"),
    path("today", views.today, name="today"),
]
