import sqlite3

con = sqlite3.connect("database.db")

dance_styles = con.execute("SELECT id FROM dance_styles").fetchall()
levels = con.execute("SELECT id FROM levels").fetchall()
locations = con.execute("SELECT id FROM locations").fetchall()

for i in range(10000):
    user_id = 2
    dance_style_id = dance_styles[i % len(dance_styles)][0]
    level_id = levels[i % len(levels)][0]
    location_id = locations[i % len(locations)][0]

    cursor = con.execute("""
        INSERT INTO projects
        (title, description, dance_style_id, level_id, user_id)
        VALUES (?, ?, ?, ?, ?)
    """, (
        f"Testiprojekti {i + 1}",
        "Testiprojekti suuren tietomäärän testaamista varten.",
        dance_style_id,
        level_id,
        user_id
    ))

    project_id = cursor.lastrowid

    con.execute("""
        INSERT INTO project_locations (project_id, location_id)
        VALUES (?, ?)
    """, (project_id, location_id))

con.commit()
con.close()