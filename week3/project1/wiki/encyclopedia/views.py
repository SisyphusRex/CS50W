from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def display(request, title):
    return render(
        request,
        "encyclopedia/display.html",
        {"title": util.get_entry(title)},
    )
