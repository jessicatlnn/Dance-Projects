import db

def add_item(title, description, dance_style_id, user_id):
    sql = """INSERT INTO items (title, description, dance_style_id, user_id)
             VALUES (?, ?, ?, ?)"""
    db.execute(sql, [title, description, dance_style_id, user_id])

def get_items():
    sql = "SELECT id, title FROM items ORDER BY id DESC"
    return db.query(sql)

def get_item(item_id):
    sql = """SELECT items.title,
                    items.description,
                    dance_styles.name AS dance_style,
                    users.username
            FROM items, users, dance_styles
            WHERE items.user_id = users.id AND
                  items.id = ?
                  AND items.dance_style_id = dance_styles.id"""
    return db.query(sql, [item_id])[0]