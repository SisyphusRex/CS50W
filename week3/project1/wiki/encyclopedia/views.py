from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util

import markdown2


class SearchForm(forms.Form):
    search = forms.CharField(label="New Search")


def index(request):

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search_title = form.cleaned_data["search"]
            text = util.get_entry(search_title)
            if text is None:
                return render(
                    request,
                    "encyclopedia/entryNotFound.html",
                    {
                        "title": search_title,
                    },
                )
            else:
                return render(
                    request,
                    "encyclopedia/display.html",
                    {
                        "title": search_title,
                        "text": markdown2.markdown(text),
                    },
                )
    else:
        return render(
            request,
            "encyclopedia/index.html",
            {
                "entries": util.list_entries(),
                "search_form": SearchForm(),
            },
        )


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
