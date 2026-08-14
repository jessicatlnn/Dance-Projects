import db

def add_project(title, description, dance_style_id, level_id, location_ids, user_id):
    sql = """INSERT INTO projects (title, description, dance_style_id, level_id, user_id)
             VALUES (?, ?, ?, ?, ?)"""

    db.execute(sql, [title, description, dance_style_id, level_id, user_id])

    project_id = db.last_insert_id()

    for location_id in location_ids:
        sql = """INSERT INTO project_locations (project_id, location_id)
                 VALUES (?, ?)"""
        db.execute(sql, [project_id, location_id])

def get_projects():
    sql = "SELECT id, title FROM projects ORDER BY id DESC"
    return db.query(sql)

def get_project(project_id):
    sql = """SELECT projects.id,
                    projects.title,
                    projects.description,
                    projects.dance_style_id,
                    projects.level_id,
                    levels.name AS level,
                    dance_styles.name AS dance_style,
                    users.id user_id,
                    users.username
            FROM projects
            JOIN users ON projects.user_id = users.id
            JOIN dance_styles ON projects.dance_style_id = dance_styles.id
            JOIN levels ON projects.level_id = levels.id
            WHERE projects.id = ?"""
    result = db.query(sql, [project_id])
    return result[0] if result else None

def get_project_locations(project_id):
    sql = """SELECT locations.id, locations.name
             FROM project_locations
             JOIN locations ON project_locations.location_id = locations.id
             WHERE project_locations.project_id = ?"""
    return db.query(sql, [project_id])

def update_project(project_id, title, description, dance_style_id, level_id, location_ids):
    sql = """UPDATE projects SET title = ?,
                              description = ?,
                              dance_style_id = ?,
                              level_id = ?
             WHERE id = ?"""
    db.execute(sql, [title, description, dance_style_id, level_id, project_id ])

    sql = "DELETE FROM project_locations WHERE project_id = ?"
    db.execute(sql, [project_id])

    for location_id in location_ids:
        sql = """INSERT INTO project_locations (project_id, location_id)
                 VALUES (?, ?)"""
        db.execute(sql, [project_id, location_id])

def remove_project(project_id):
    sql = "DELETE FROM project_locations WHERE project_id = ?"
    db.execute(sql, [project_id])

    sql = "DELETE FROM projects WHERE id = ?"
    db.execute(sql, [project_id])

def find_projects(query):
    sql = """SELECT id, title
             FROM projects
             WHERE title LIKE ? OR description LIKE ?
             ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like])

def add_participant(project_id, user_id, full_name):
    sql = """INSERT INTO participants (project_id, user_id, name) VALUES (?, ?, ?)"""
    db.execute(sql, [project_id, user_id, full_name])

def get_participants(project_id):
    sql = """SELECT participants.name,
                    users.id AS user_id,
                    users.username
             FROM participants, users
             WHERE participants.project_id = ?
             AND participants.user_id = users.id
             ORDER BY participants.id"""

    result = db.query(sql, [project_id])
    print("PARTICIPANT RESULT:", result)
    return result