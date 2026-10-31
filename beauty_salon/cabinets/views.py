from django.shortcuts import render

from beauty import db


def cabinet_list(request):
    try:
        cabinets = db.get_cabinets()
    except db.DatabaseError:
        return render(request, "error.html", status=500)
    return render(request, "cabinets/cabinet_list.html", {"cabinets": cabinets})
