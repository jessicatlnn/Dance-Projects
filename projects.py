import db

def add_project(title, description, dance_style_id, level, location_ids, user_id):
    sql = """INSERT INTO projects (title, description, dance_style_id, level, user_id)
             VALUES (?, ?, ?, ?, ?)"""

    db.execute(sql, [title, description, dance_style_id, level, user_id])

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
                    projects.level,
                    dance_styles.name AS dance_style,
                    users.id user_id,
                    users.username
            FROM projects, users, dance_styles
            WHERE projects.user_id = users.id AND
                  projects.dance_style_id = dance_styles.id AND
                  projects.id = ?"""
    result = db.query(sql, [project_id])
    return result[0] if result else None

def get_project_locations(project_id):
    sql = """SELECT locations.id, locations.name
             FROM project_locations
             JOIN locations
             ON project_locations.location_id = locations.id
             WHERE project_locations.project_id = ?"""
    return db.query(sql, [project_id])

def update_project(project_id, title, description, dance_style_id, level, location_ids):
    sql = """UPDATE projects SET title = ?,
                              description = ?,
                              dance_style_id = ?,
                              level = ?
             WHERE id = ?"""
    db.execute(sql, [title, description, dance_style_id, level, project_id ])

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