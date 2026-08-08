import db

def add_project(title, description, dance_style_id, user_id):
    sql = """INSERT INTO projects (title, description, dance_style_id, user_id)
             VALUES (?, ?, ?, ?)"""
    db.execute(sql, [title, description, dance_style_id, user_id])

def get_projects():
    sql = "SELECT id, title FROM projects ORDER BY id DESC"
    return db.query(sql)

def get_project(project_id):
    sql = """SELECT projects.id,
                    projects.title,
                    projects.description,
                    projects.dance_style_id,
                    dance_styles.name AS dance_style,
                    users.id user_id,
                    users.username
            FROM projects, users, dance_styles
            WHERE projects.user_id = users.id AND
                  projects.dance_style_id = dance_styles.id AND
                  projects.id = ?"""
    return db.query(sql, [project_id])[0]

def update_project(project_id, title, description, dance_style_id):
    sql = """UPDATE projects SET title = ?,
                              description = ?,
                              dance_style_id = ?
                          WHERE id = ?"""
    db.execute(sql, [title, description, dance_style_id, project_id ])

def remove_project(project_id):
    sql = "DELETE FROM projects WHERE id = ?"
    db.execute(sql, [project_id])

def find_projects(query):
    sql = """SELECT id, title
             FROM projects
             WHERE title LIKE ? OR description LIKE ?
             ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like])