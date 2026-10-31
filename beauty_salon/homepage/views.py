from django.shortcuts import render

from beauty import db


def home(request):
    try:
        visits = db.get_visits()
    except db.DatabaseError:
        return render(request, "error.html", status=500)
    return render(request, "homepage/home.html", {"visits": visits})
