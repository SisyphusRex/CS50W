from django.shortcuts import render
import datetime

# Create your views here.


def index(request):
    """index function for app"""
    now = datetime.datetime.now()
    return render(
        request, "newyear/index.html", {"newyear": now.month == 1 and now.day == 1}
    )
    # in the above render function, we are passing the variable "newyear" into the template "newyear/index.html"
