import secrets
import sqlite3
from flask import Flask
from flask import redirect, abort, render_template, request, session
import db
import config
import projects
import users


app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
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
    participants = projects.get_participants(project_id)

    return render_template("show_project.html", project=project, locations=locations, participants=participants)

@app.route("/new_participant", methods=["POST"])
def new_participant():
    require_login()
    check_csrf()

    project_id = request.form["project_id"]
    project = projects.get_project(project_id)
    if not project:
        abort(404)

    name = request.form["participant_name"].strip()
    surname = request.form["participant_surname"].strip()
    if not name or not surname:
        abort(400)
    full_name = name + " " + surname

    user_id = session["user_id"]

    projects.add_participant(project_id, user_id, full_name)

    return redirect("/project/" + str(project_id))

@app.route("/new_project")
def new_project():
    require_login()
    dance_styles = db.query("SELECT id, name FROM dance_styles ORDER BY CASE WHEN name = 'Muu' THEN 1 ELSE 0 END, name")
    levels = db.query("SELECT id, name FROM levels")
    locations = db.query("SELECT id, name FROM locations ORDER BY name = 'Muu', name")
    return render_template("new_project.html", dance_styles=dance_styles, levels=levels, locations=locations)

@app.route("/create_project", methods=["POST"])
def create_project():
    require_login()
    check_csrf()

    dance_styles = db.query("SELECT id, name FROM dance_styles ORDER BY CASE WHEN name = 'Muu' THEN 1 ELSE 0 END, name")
    levels = db.query("SELECT id, name FROM levels")
    locations = db.query("SELECT id, name FROM locations ORDER BY name = 'Muu', name")

    title = request.form["title"]
    if len(title) > 50:
        abort(403)
    if len(title) < 3:
        return render_template(
            "new_project.html", error="Otsikon täytyy olla vähintään 3 merkkiä pitkä", dance_styles=dance_styles, levels=levels, locations=locations)

    description = request.form["description"]
    if len(description) > 1000:
        abort(403)
    if len(description) < 3:
        return render_template(
            "new_project.html", error="Kuvauksen täytyy olla vähintään 3 merkkiä pitkä", dance_styles=dance_styles, levels=levels, locations=locations)

    dance_style_id = request.form["dance_style"]

    level_id = request.form["level"]
    if not level_id:
        return render_template(
            "new_project.html", error="Valitse taso", dance_styles=dance_styles, levels=levels, locations=locations)

    location_ids = request.form.getlist("locations")
    if not location_ids:
        return render_template("new_project.html", error="Valitse vähintään yksi sijainti", dance_styles=dance_styles, levels=levels, locations=locations)

    user_id = session["user_id"]

    projects.add_project(title, description, dance_style_id, level_id, location_ids, user_id)

    return redirect("/")

@app.route("/edit_project/<int:project_id>")
def edit_project(project_id):
    require_login()

    project = projects.get_project(project_id)
    if not project:
        abort(404)

    dance_styles = db.query("SELECT id, name FROM dance_styles ORDER BY CASE WHEN name = 'Muu' THEN 1 ELSE 0 END, name")
    levels = db.query("SELECT id, name FROM levels")
    locations = db.query("SELECT id, name FROM locations ORDER BY name = 'Muu', name")

    project_locations = projects.get_project_locations(project_id)
    project_location_ids = [location["id"] for location in project_locations]

    if project["user_id"] != session["user_id"]:
        abort(403)

    return render_template("edit_project.html", project=project, dance_styles=dance_styles, levels=levels, locations=locations, project_location_ids=project_location_ids)

@app.route("/update_project", methods=["POST"])
def update_project():
    require_login()
    check_csrf()


    project_id = request.form["project_id"]

    project = projects.get_project(project_id)
    if not project:
        abort(404)

    project_locations = projects.get_project_locations(project_id)
    project_location_ids = [location["id"] for location in project_locations]

    if project["user_id"] != session["user_id"]:
        abort(403)

    dance_styles = db.query("SELECT id, name FROM dance_styles ORDER BY CASE WHEN name = 'Muu' THEN 1 ELSE 0 END, name")
    levels = db.query("SELECT id, name FROM levels")
    locations = db.query("SELECT id, name FROM locations ORDER BY name = 'Muu', name")

    title = request.form["title"]

    if len(title) > 50:
        abort(403)
    if len(title) < 3:
        return render_template("edit_project.html", project=project, dance_styles=dance_styles, levels=levels, locations=locations, project_location_ids=project_location_ids,
                                error="Otsikon täytyy olla vähintään 3 merkkiä pitkä")

    description = request.form["description"]
    if len(description) > 1000:
        abort(403)
    if len(description) < 3:
        return render_template("edit_project.html", project=project, dance_styles=dance_styles, levels=levels, locations=locations, project_location_ids=project_location_ids,
                                error="Kuvauksen täytyy olla vähintään 3 merkkiä pitkä")

    dance_style_id = request.form["dance_style"]

    level_id = request.form["level"]
    if not level_id:
        return render_template(
            "edit_project.html", project=project, error="Valitse taso", dance_styles=dance_styles, levels=levels, locations=locations, project_location_ids=project_location_ids)

    location_ids = request.form.getlist("locations")
    if not location_ids:
        return render_template("edit_project.html", project=project, dance_styles=dance_styles, levels=levels, locations=locations, project_location_ids=project_location_ids,
        error="Valitse vähintään yksi sijainti")

    projects.update_project(project_id, title, description, dance_style_id, level_id, location_ids)

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
        check_csrf()
        if "remove" in request.form:
            projects.remove_project(project_id)
            return redirect("/")
        else:
            return redirect("/project/" + str(project_id))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if len(username) < 3:
        return render_template("register.html",
                                error="Käyttäjänimen täytyy olla vähintään 3 merkkiä pitkä",
                                username=username)
    if " " in username:
        return render_template("register.html",
                                error="Käyttäjänimessä ei saa olla välilyöntejä",
                                username=username)
    if len(password1) < 6:
        return render_template("register.html",
                                error="Salasanan täytyy olla vähintään 6 merkkiä pitkä",
                                username=username)
    if password1 != password2:
        return render_template("register.html",
                                error="Salasanat eivät täsmää",
                                username=username)

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        return render_template("register.html", error="Tunnus on jo varattu")
    return render_template("login.html",
                            message="Tunnus luotu onnistuneesti.")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)

        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            return render_template("login.html",
                                    error="Väärä käyttäjätunnus tai salasana",
                                    username=username)

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
        del session["csrf_token"]
    return redirect("/")
