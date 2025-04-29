from django.shortcuts import render

from . import util

import markdown2


def index(request):
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
