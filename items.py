import db

def add_item(title, description, dance_style_id, user_id):
    sql = """INSERT INTO items (title, description, dance_style_id, user_id)
             VALUES (?, ?, ?, ?)"""
    db.execute(sql, [title, description, dance_style_id, user_id])

def get_items():
    sql = "SELECT id, title FROM items ORDER BY id DESC"
    return db.query(sql)

def get_item(item_id):
    sql = """SELECT items.id,
                    items.title,
                    items.description,
                    items.dance_style_id,
                    dance_styles.name AS dance_style,
                    users.id user_id,
                    users.username
            FROM items, users, dance_styles
            WHERE items.user_id = users.id AND
                  items.dance_style_id = dance_styles.id AND
                  items.id = ?"""
    return db.query(sql, [item_id])[0]

def update_item(item_id, title, description, dance_style_id):
    sql = """UPDATE items SET title = ?,
                              description = ?,
                              dance_style_id = ?
                          WHERE id = ?"""
    db.execute(sql, [title, description, dance_style_id, item_id ])

def remove_item(item_id):
    sql = "DELETE FROM items WHERE id = ?"
    db.execute(sql, [item_id])

def find_items(query):
    sql = """SELECT id, title
             FROM items
             WHERE title LIKE ? OR description LIKE ?
             ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like])