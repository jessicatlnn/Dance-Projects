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

CREATE TABLE levels (
    id INTEGER PRIMARY KEY,
    name TEXT
);

INSERT INTO levels (id, name) VALUES
(1, 'Alkeistaso'),
(2, 'Keskitaso'),
(3, 'Jatkotaso'),
(4, 'Ammattilaistaso'),
(5, 'Avoin taso');

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

CREATE TABLE projects (
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
    creation_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    dance_style_id INTEGER REFERENCES dance_styles(id),
    level_id INTEGER REFERENCES levels(id),
    user_id INTEGER REFERENCES users
);

CREATE TABLE project_locations (
    project_id INTEGER REFERENCES projects(id),
    location_id INTEGER REFERENCES locations(id),
    PRIMARY KEY (project_id, location_id)
);

CREATE TABLE participants (
    id INTEGER PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    user_id INTEGER REFERENCES users(id)
);

CREATE TABLE participation_requests (
    id INTEGER PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    user_id INTEGER REFERENCES users(id),
    status TEXT
);