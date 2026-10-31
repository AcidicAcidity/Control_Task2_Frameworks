from django.shortcuts import render

from . import db


def _positive_int(value, maximum=1000):
    """Возвращает int >= 1 или None, если значение пустое/некорректное."""
    try:
        number = int(value)
    except (TypeError, ValueError):
        return None
    return number if 1 <= number <= maximum else None


def visit_list(request):
    raw_clients = request.GET.get("clients", "").strip()
    raw_limit = request.GET.get("limit", "").strip()
    sort = request.GET.get("sort", db.DEFAULT_SORT)
    if sort not in db.SORT_OPTIONS:
        sort = db.DEFAULT_SORT

    min_clients = _positive_int(raw_clients)
    limit = _positive_int(raw_limit, 100)
    input_error = None
    if (raw_clients and min_clients is None) or (raw_limit and limit is None):
        input_error = "Введите целое положительное число — фильтр не применён."

    try:
        visits = db.get_visits(min_clients=min_clients or 0, sort=sort, limit=limit)
    except db.DatabaseError:
        return render(request, "error.html", status=500)

    return render(request, "beauty/visit_list.html", {
        "visits": visits,
        "clients": raw_clients,
        "limit": raw_limit,
        "sort": sort,
        "sort_options": [(k, v[0]) for k, v in db.SORT_OPTIONS.items()],
        "input_error": input_error,
        "filtered": bool(min_clients or limit),
    })


def visit_detail(request, slug):
    try:
        visit = db.get_visit_by_slug(slug)
    except db.DatabaseError:
        return render(request, "error.html", status=500)
    if visit is None:
        return render(request, "404.html", {"slug": slug}, status=404)
    return render(request, "beauty/visit_detail.html", {"visit": visit})


def statistics(request):
    raw = request.GET.get("min", "").strip()
    min_count = _positive_int(raw) or 3          # по умолчанию показываем типы с >= 3 визитами
    try:
        stats = db.get_statistics(min_count)
        total = db.count_visits()
    except db.DatabaseError:
        return render(request, "error.html", status=500)
    return render(request, "beauty/statistics.html",
                  {"stats": stats, "min_count": min_count, "total": total})
