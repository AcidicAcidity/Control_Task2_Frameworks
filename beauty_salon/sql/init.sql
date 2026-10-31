DROP TABLE IF EXISTS beauty;
DROP TABLE IF EXISTS cabinets;

CREATE TABLE cabinets (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT    NOT NULL,
    capacity      INTEGER NOT NULL CHECK (capacity > 0),
    cabin_profile TEXT    NOT NULL
);

CREATE TABLE beauty (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    title        TEXT    NOT NULL,
    slug         TEXT    NOT NULL UNIQUE,
    service_type TEXT    NOT NULL,
    visit_date   TEXT    NOT NULL,           -- 'YYYY-MM-DD HH:MM'
    duration     INTEGER NOT NULL,           -- минуты
    clients      INTEGER NOT NULL,
    status       TEXT    NOT NULL,           -- запланирован / обслуживается / завершён
    cabin_id     INTEGER REFERENCES cabinets(id)
);

INSERT INTO cabinets (name, capacity, cabin_profile) VALUES
 ('Кабинет 1', 4, 'парикмахерская'),
 ('Кабинет 2', 3, 'маникюр'),
 ('Кабинет 3', 2, 'косметология'),
 ('Кабинет 4', 5, 'парикмахерская');

INSERT INTO beauty (title, slug, service_type, visit_date, duration, clients, status, cabin_id) VALUES
 ('Стрижка и укладка',        'haircut-styling',  'стрижка',     '2026-10-15 10:00',  60, 1, 'запланирован', 1),
 ('Мужская стрижка',          'mens-haircut',     'стрижка',     '2026-10-15 12:00',  40, 1, 'завершён',     1),
 ('Детская стрижка для двоих','kids-haircut',     'стрижка',     '2026-10-16 11:00',  45, 2, 'запланирован', 4),
 ('Окрашивание в технике балаяж с уходом и тонированием', 'balayage-coloring', 'окрашивание', '2026-10-17 14:00', 180, 1, 'обслуживается', 1),
 ('Свадебное окрашивание',    'wedding-coloring', 'окрашивание', '2026-10-18 09:00', 150, 3, 'запланирован', 4),
 ('Классический маникюр',     'classic-manicure', 'маникюр',     '2026-10-14 15:00',  60, 1, 'завершён',     2),
 ('Маникюр с покрытием',      'gel-manicure',     'маникюр',     '2026-10-19 16:30',  90, 2, 'запланирован', 2),
 ('Семейный маникюр',         'family-manicure',  'маникюр',     '2026-10-20 13:00', 120, 4, 'обслуживается', 2),
 ('Экспресс-стрижка',         'express-haircut',  'стрижка',     '2026-10-21 17:00',  20, 1, 'запланирован', NULL);
