-- Все запросы реально используются в beauty/db.py. Знак ? — параметр (параметризованный запрос).

-- 1. Список визитов + кабинет (JOIN)                         -> db.get_visits()
SELECT v.id, v.title, v.slug, v.service_type, v.visit_date, v.duration, v.clients, v.status,
       v.cabin_id, c.name AS cabin_name, c.capacity AS cabin_capacity, c.cabin_profile
FROM beauty v LEFT JOIN cabinets c ON c.id = v.cabin_id;

-- 2. Выборка по условию (минимум клиентов, GET ?clients=)    -> db.get_visits(min_clients=...)
--    ... WHERE v.clients >= ?

-- 3. Сортировка и ограничение (ORDER BY из белого списка, LIMIT ?)
--    ... ORDER BY v.visit_date DESC LIMIT ?

-- 4. Один визит по slug с данными кабинета                   -> db.get_visit_by_slug()
--    ... WHERE v.slug = ?

-- 5. Кабинеты                                                -> db.get_cabinets()
SELECT id, name, capacity, cabin_profile FROM cabinets ORDER BY id;

-- 6. Общее количество визитов (COUNT)                        -> db.count_visits()
SELECT COUNT(*) AS total FROM beauty;

-- 7. Статистика: COUNT + GROUP BY + HAVING                   -> db.get_statistics(min_count)
SELECT service_type, COUNT(*) AS visits_count, SUM(clients) AS total_clients
FROM beauty
GROUP BY service_type
HAVING COUNT(*) >= ?
ORDER BY visits_count DESC, service_type;
