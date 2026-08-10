import sqlite3
from flask import Flask
from flask import redirect, abort, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import db
import config
import projects
import users


app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    all_projects = projects.get_projects()
    return render_template("index.html", projects=all_projects)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    projects = users.get_projects(user_id)
    return render_template("show_user.html", user=user, projects=projects)

@app.route("/find_project")
def find_project():
    query = request.args.get("query")
    if query:
        results = projects.find_projects(query)
    else:
        query = ""
        results = []
    return render_template("find_project.html", query=query, results=results)

@app.route("/project/<int:project_id>")
def show_project(project_id):
    project = projects.get_project(project_id)
    if not project:
        abort(404)
    locations = projects.get_project_locations(project_id)
    return render_template("show_project.html", project=project, locations=locations)

@app.route("/new_project")
def new_project():
    require_login()
    dance_styles = db.query("SELECT id, name FROM dance_styles")
    locations = db.query("SELECT id, name FROM locations ORDER BY name = 'Muu', name")
    return render_template("new_project.html", dance_styles=dance_styles, locations=locations)

@app.route("/create_project", methods=["POST"])
def create_project():
    require_login()

    dance_styles = db.query("SELECT id, name FROM dance_styles")
    locations = db.query("SELECT id, name FROM locations ORDER BY name = 'Muu', name")

    title = request.form["title"]
    if len(title) > 50:
        abort(403)
    if len(title) < 3:
        return render_template(
            "new_project.html", error="Otsikon täytyy olla vähintään 3 merkkiä pitkä", dance_styles=dance_styles, locations=locations)

    description = request.form["description"]
    if len(description) > 1000:
        abort(403)
    if len(description) < 3:
        return render_template(
            "new_project.html", error="Kuvauksen täytyy olla vähintään 3 merkkiä pitkä", dance_styles=dance_styles, locations=locations)

    dance_style_id = request.form["dance_style"]

    location_ids = request.form.getlist("locations")
    if not location_ids:
        return render_template("new_project.html", error="Valitse vähintään yksi sijainti", dance_styles=dance_styles, locations=locations)

    user_id = session["user_id"]

    projects.add_project(title, description, dance_style_id, location_ids, user_id)

    return redirect("/")

@app.route("/edit_project/<int:project_id>")
def edit_project(project_id):
    require_login()

    project = projects.get_project(project_id)
    if not project:
        abort(404)

    dance_styles = db.query("SELECT id, name FROM dance_styles")
    locations = db.query("SELECT id, name FROM locations ORDER BY name = 'Muu', name")

    project_locations = projects.get_project_locations(project_id)
    project_location_ids = [location["id"] for location in project_locations]

    if project["user_id"] != session["user_id"]:
        abort(403)

    return render_template("edit_project.html", project=project, dance_styles=dance_styles, locations=locations, project_location_ids=project_location_ids)

@app.route("/update_project", methods=["POST"])
def update_project():
    require_login()

    project_id = request.form["project_id"]
    project = projects.get_project(project_id)
    project_locations = projects.get_project_locations(project_id)
    project_location_ids = [location["id"] for location in project_locations]
    if not project:
        abort(404)
    if project["user_id"] != session["user_id"]:
        abort(403)

    dance_styles = db.query("SELECT id, name FROM dance_styles")
    locations = db.query("SELECT id, name FROM locations ORDER BY name = 'Muu', name")

    title = request.form["title"]

    if len(title) > 50:
        abort(403)
    if len(title) < 3:
        return render_template("edit_project.html", project=project, dance_styles=dance_styles, locations=locations, project_location_ids=project_location_ids,
                                error="Otsikon täytyy olla vähintään 3 merkkiä pitkä")

    description = request.form["description"]
    if len(description) > 1000:
        abort(403)
    if len(description) < 3:
        return render_template("edit_project.html", project=project, dance_styles=dance_styles, locations=locations, project_location_ids=project_location_ids,
                                error="Kuvauksen täytyy olla vähintään 3 merkkiä pitkä")

    dance_style_id = request.form["dance_style"]

    location_ids = request.form.getlist("locations")
    if not location_ids:
        project_locations = projects.get_project_locations(project_id)
        project_location_ids = [location["id"] for location in project_locations]
        return render_template("edit_project.html", project=project, dance_styles=dance_styles, locations=locations, project_location_ids=project_location_ids,
        error="Valitse vähintään yksi sijainti")

    projects.update_project(project_id, title, description, dance_style_id, location_ids)

    return redirect("/project/" + str(project_id))

@app.route("/remove_project/<int:project_id>", methods=["GET", "POST"])
def remove_project(project_id):
    require_login()

    project = projects.get_project(project_id)
    if not project:
        abort(404)
    if project["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_project.html", project=project)

    if request.method == "POST":
        if "remove" in request.form:
            projects.remove_project(project_id)
            return redirect("/")
        else:
            return redirect("/project/" + str(project_id))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/registration_complete")
def registration_complete():
    return render_template("registration_complete.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if len(username) < 3:
        return render_template("register.html", error="Käyttäjänimen täytyy olla vähintään 3 merkkiä pitkä")
    if " " in username:
        return render_template("register.html", error="Käyttäjänimessä ei saa olla välilyöntejä")
    if len(password1) < 6:
        return render_template("register.html", error="Salasanan täytyy olla vähintään 6 merkkiä pitkä")
    if password1 != password2:
        return render_template("register.html", error="Salasanat eivät ole samat")
    
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return render_template("register.html", error="Tunnus on jo varattu")

    return redirect("/registration_complete")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])

        if not result:
            return render_template("login.html", error="Väärä käyttäjätunnus tai salasana")

        user = result[0]
        user_id = user["id"]

        password_hash = user["password_hash"]
        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return render_template("login.html", error="Väärä käyttäjätunnus tai salasana")

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")