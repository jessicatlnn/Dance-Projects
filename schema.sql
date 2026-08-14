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

CREATE TABLE projects (
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
    dance_style_id INTEGER REFERENCES dance_styles(id),
    level TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE locations (
    id INTEGER PRIMARY KEY,
    name TEXT
);

INSERT INTO locations (id, name) VALUES
(1, 'Helsinki'),
(2, 'Vantaa'),
(3, 'Espoo'),
(4, 'Kerava'),
(5, 'Tampere'),
(6, 'Turku'),
(7, 'Rovaniemi'),
(8, 'Muu');

CREATE TABLE project_locations (
    project_id INTEGER REFERENCES projects(id),
    location_id INTEGER REFERENCES locations(id),
    PRIMARY KEY (project_id, location_id)
);
