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
            return HttpResponseRedirect(reverse("display", args=(search_title,)))
        else:
            return render(
                request,
                "encyclopedia/index.html",
                {
                    "entries": util.list_entries(),
                    "search_form": SearchForm(),
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

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search_title = form.cleaned_data["search"]
            return HttpResponseRedirect(reverse("display", args=(search_title,)))
        else:
            return HttpResponseRedirect(reverse("display", args=(title,)))
    text = util.get_entry(title)

    if text is None:
        return render(
            request,
            "encyclopedia/entryNotFound.html",
            {
                "title": title,
                "search_form": SearchForm(),
            },
        )
    else:
        return render(
            request,
            "encyclopedia/display.html",
            {
                "title": title,
                "text": markdown2.markdown(text),
                "search_form": SearchForm(),
            },
        )
