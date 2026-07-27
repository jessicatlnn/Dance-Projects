CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE dance_styles (
    id INTEGER PRIMARY KEY,
    name TEXT
);

INSERT INTO dance_styles (id, name) VALUES
(1, 'Hip Hop'),
(2, 'Commercial'),
(3, 'Nykytanssi'),
(4, 'Heels'),
(5, 'Jazz'),
(6, 'Baletti'),
(7, 'Muu');

CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
    dance_style_id INTEGER REFERENCES dance_styles(id),
    user_id INTEGER REFERENCES users
);
