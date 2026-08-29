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
    sql = """SELECT projects.id,
                    projects.title,
                    projects.creation_date,
                    users.username
             FROM projects
             JOIN users ON projects.user_id = users.id
             ORDER BY projects.id DESC"""
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

def get_projects(page):
    projects_per_page = 10
    offset = (page - 1) * projects_per_page

    sql = """SELECT projects.id,
                    projects.title,
                    projects.creation_date,
                    users.username
             FROM projects
             JOIN users ON projects.user_id = users.id
             ORDER BY projects.id DESC
             LIMIT ? OFFSET ?"""

    return db.query(sql, [projects_per_page, offset])

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
    sql ="DELETE FROM participants WHERE project_id = ?"
    db.execute(sql, [project_id])

    sql ="DELETE FROM participation_requests WHERE project_id = ?"
    db.execute(sql, [project_id])

    sql = "DELETE FROM project_locations WHERE project_id = ?"
    db.execute(sql, [project_id])

    sql = "DELETE FROM projects WHERE id = ?"
    db.execute(sql, [project_id])

def find_projects(query, dance_style_id, level_id, location_id, page):
    projects_per_page = 10
    offset = (page - 1) * projects_per_page

    sql = """SELECT projects.id, projects.title, projects.creation_date, users.username
             FROM projects
             JOIN users ON projects.user_id = users.id
             WHERE 1=1"""
    parameters = []

    if query:
        sql += """ AND (LOWER(projects.title) LIKE ?
                      OR LOWER(projects.description) LIKE ?)"""
        like = "%" + query.lower() + "%"
        parameters.extend([like, like])

    if dance_style_id:
        sql += " AND projects.dance_style_id = ?"
        parameters.append(dance_style_id)

    if level_id:
        sql += " AND projects.level_id = ?"
        parameters.append(level_id)

    if location_id:
        sql += """ AND projects.id IN (
                      SELECT project_id
                      FROM project_locations
                      WHERE location_id = ?
                  )"""
        parameters.append(location_id)

    sql += " ORDER BY projects.id DESC LIMIT ? OFFSET ?"
    parameters.extend([projects_per_page, offset])

    return db.query(sql, parameters)

def get_dance_styles():
    sql = """SELECT id, name
             FROM dance_styles
             ORDER BY CASE WHEN name = 'Muu' THEN 1 ELSE 0 END, name"""
    return db.query(sql)

def get_levels():
    sql = """SELECT id, name
             FROM levels"""
    return db.query(sql)

def get_locations():
    sql = """SELECT id, name
             FROM locations
             ORDER BY name = 'Muu', name"""
    return db.query(sql)


# PARTICIPATION

def get_participants(project_id):
    sql = """SELECT users.id AS user_id,
                    users.username
             FROM participants, users
             WHERE participants.project_id = ?
             AND participants.user_id = users.id
             ORDER BY participants.id"""

    result = db.query(sql, [project_id])
    return result

def add_participation_request(project_id, user_id):
    sql = """INSERT INTO participation_requests
             (project_id, user_id, status)
             VALUES (?, ?, ?)"""
    db.execute(sql, [project_id, user_id, "pending"])

def get_project_participation_requests(project_id):
    sql = """SELECT participation_requests.id,
             participation_requests.user_id,
             users.username
             FROM participation_requests
             JOIN users ON participation_requests.user_id = users.id
             WHERE participation_requests.project_id = ?
             AND participation_requests.status = 'pending'"""
    return db.query(sql, [project_id])

def get_participation_request(request_id):
    sql = """SELECT id, project_id, user_id, status
             FROM participation_requests
             WHERE id = ?"""

    result = db.query(sql, [request_id])

    if result:
        return result[0]

    return None

def accept_participation_request(request_id):
    participation_request = get_participation_request(request_id)

    sql = """INSERT INTO participants (project_id, user_id)
             VALUES (?, ?)"""

    db.execute(sql, [participation_request["project_id"], participation_request["user_id"]])

    sql = """UPDATE participation_requests
             SET status = 'accepted'
             WHERE id = ?"""

    db.execute(sql, [request_id])

def reject_participation_request(request_id):
    sql = """UPDATE participation_requests
             SET status = 'rejected'
             WHERE id = ?"""

    db.execute(sql, [request_id])