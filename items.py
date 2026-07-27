import db

def add_item(title, description, dance_style_id, user_id):
    sql = """INSERT INTO items (title, description, dance_style_id, user_id)
             VALUES (?, ?, ?, ?)"""
    db.execute(sql, [title, description, dance_style_id, user_id])