from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.display, name="display"),
    path("create_new/", views.create_new, name="create"),
    path("edit/<str:title>", views.edit_existing, name="edit"),
    path("random/", views.random1, name="random1"),
]
