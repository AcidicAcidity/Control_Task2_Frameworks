"""Работа с SQLite через sqlite3 (без Django ORM)."""
import os
import sqlite3
from datetime import datetime

from django.conf import settings


class DatabaseError(Exception):
    """Ошибка доступа к БД (без технических деталей для пользователя)."""


def get_connection():
    path = str(settings.DB_PATH)
    if not os.path.exists(path):          # не даём sqlite3 молча создать пустой файл
        raise DatabaseError("database file not found")
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _prepare(row):
    item = dict(row)
    if item.get("visit_date"):
        item["visit_date"] = datetime.strptime(item["visit_date"], "%Y-%m-%d %H:%M")
    return item


def execute(sql, params=()):
    """Выполняет запрос с параметрами, возвращает список словарей, всегда закрывает соединение."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.execute(sql, params)          # параметры передаются отдельно от SQL
        return [_prepare(r) for r in cursor.fetchall()]
    except (sqlite3.Error, ValueError) as exc:
        raise DatabaseError(str(exc)) from exc
    finally:
        if conn is not None:
            conn.close()


VISITS_SQL = """
SELECT v.id, v.title, v.slug, v.service_type, v.visit_date, v.duration, v.clients, v.status,
       v.cabin_id, c.name AS cabin_name, c.capacity AS cabin_capacity, c.cabin_profile
FROM beauty v
LEFT JOIN cabinets c ON c.id = v.cabin_id
"""

# Белый список сортировок: пользователь выбирает КЛЮЧ, а не SQL-фрагмент
SORT_OPTIONS = {
    "date_asc":      ("Дата: сначала ранние",     "v.visit_date ASC"),
    "date_desc":     ("Дата: сначала поздние",    "v.visit_date DESC"),
    "clients_desc":  ("Клиентов: по убыванию",    "v.clients DESC, v.visit_date ASC"),
    "duration_desc": ("Длительность: по убыванию", "v.duration DESC, v.visit_date ASC"),
    "title":         ("Название: А–Я",            "v.title ASC"),
}
DEFAULT_SORT = "date_asc"


def get_visits(min_clients=0, sort=DEFAULT_SORT, limit=None):
    order_by = SORT_OPTIONS.get(sort, SORT_OPTIONS[DEFAULT_SORT])[1]
    sql = VISITS_SQL + " WHERE v.clients >= ? ORDER BY " + order_by   # order_by — только из словаря
    params = [min_clients or 0]
    if limit:
        sql += " LIMIT ?"
        params.append(limit)
    return execute(sql, params)


def get_visit_by_slug(slug):
    rows = execute(VISITS_SQL + " WHERE v.slug = ?", (slug,))
    return rows[0] if rows else None


def get_cabinets():
    return execute("SELECT id, name, capacity, cabin_profile FROM cabinets ORDER BY id")


def count_visits():
    return execute("SELECT COUNT(*) AS total FROM beauty")[0]["total"]


def get_statistics(min_count=1):
    return execute(
        """SELECT service_type, COUNT(*) AS visits_count, SUM(clients) AS total_clients
           FROM beauty
           GROUP BY service_type
           HAVING COUNT(*) >= ?
           ORDER BY visits_count DESC, service_type""",
        (min_count,),
    )
