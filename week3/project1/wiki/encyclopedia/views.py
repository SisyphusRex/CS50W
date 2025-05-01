from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import random

from . import util

import markdown2


class SearchForm(forms.Form):
    search = forms.CharField(label="New Search")


class NewForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Title"}), label="New Title"
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Content"}), label="New Content"
    )


class EditForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(), label="Edit Content")


def random1(request):
    entries = util.list_entries()
    random_choice = random.randint(0, len(entries))
    return HttpResponseRedirect(reverse("display", args=(entries[random_choice],)))


def edit_existing(request, title):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            edit_content = form.cleaned_data["content"]
            util.save_entry(title, edit_content)
            return HttpResponseRedirect(reverse("display", args=(title,)))
    else:
        content = util.get_entry(title)
        return render(
            request,
            "encyclopedia/editEntry.html",
            {
                "edit_form": EditForm(initial={"content": content}),
                "title": title,
            },
        )


def create_new(request):
    entries = util.list_entries()
    if request.method == "POST":
        form = NewForm(request.POST)
        if form.is_valid():
            new_title = form.cleaned_data["title"]
            new_content = form.cleaned_data["content"]
            for entry in entries:
                if new_title.lower() == entry.lower():
                    return render(
                        request,
                        "encyclopedia/alreadyExists.html",
                        {
                            "title": new_title,
                            "search_form": SearchForm(),
                        },
                    )
            util.save_entry(new_title, new_content)
            return HttpResponseRedirect(reverse("display", args=(new_title,)))

    else:
        return render(
            request,
            "encyclopedia/newEntry.html",
            {
                "create_form": NewForm(),
            },
        )


def index(request):
    entries = util.list_entries()
    possible_entries = []
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search_title = form.cleaned_data["search"]
            for title in entries:
                if search_title.lower() == title.lower():
                    return HttpResponseRedirect(
                        reverse("display", args=(search_title,))
                    )
                if search_title.lower() in title.lower():
                    possible_entries.append(title)
            if len(possible_entries) > 0:
                return render(
                    request,
                    "encyclopedia/search.html",
                    {
                        "possible_entries": possible_entries,
                        "search_form": SearchForm(),
                    },
                )
            else:
                return render(
                    request,
                    "encyclopedia/entryNotFound.html",
                    {
                        "title": search_title,
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

    entries = util.list_entries()
    possible_entries = []
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search_title = form.cleaned_data["search"]
            for title in entries:
                if search_title.lower() == title.lower():
                    return HttpResponseRedirect(
                        reverse("display", args=(search_title,))
                    )
                if search_title.lower() in title.lower():
                    possible_entries.append(title)
            if len(possible_entries) > 0:
                return render(
                    request,
                    "encyclopedia/search.html",
                    {
                        "possible_entries": possible_entries,
                        "search_form": SearchForm(),
                    },
                )
            else:
                return render(
                    request,
                    "encyclopedia/entryNotFound.html",
                    {
                        "title": search_title,
                        "search_form": SearchForm(),
                    },
                )
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
