from django.shortcuts import render
from django import forms

from . import util

import markdown2


class SearchForm(forms.Form):
    search = forms.CharField(label="New Search")


def index(request):

    if request.method == "POST":
        title = request.form["q"]
        text = util.get_entry(title)

        if text is None:
            return render(
                request,
                "encyclopedia/entryNotFound.html",
                {
                    "title": title,
                },
            )
        else:
            return render(
                request,
                "encyclopedia/display.html",
                {"title": title, "text": markdown2.markdown(text)},
            )

    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def display(request, title):

    text = util.get_entry(title)

    if text is None:
        return render(
            request,
            "encyclopedia/entryNotFound.html",
            {
                "title": title,
            },
        )
    else:
        return render(
            request,
            "encyclopedia/display.html",
            {"title": title, "text": markdown2.markdown(text)},
        )
