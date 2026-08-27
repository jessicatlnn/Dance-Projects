import secrets
import sqlite3
from flask import redirect, abort, render_template, request, session, Flask, flash
import config
import projects
import users


app = Flask(__name__)
app.secret_key = config.secret_key


# HELPER FUNCTIONS

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)


# ERROR HANDLING

@app.errorhandler(400)
def bad_request(e):
    return render_template("400.html"), 400

@app.errorhandler(403)
def forbidden(e):
    return render_template("403.html"), 403

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# ROUTES

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
    participation_requests = projects.get_project_participation_requests(project_id)

    return render_template("show_project.html",
                            project=project,
                            locations=locations,
                            participants=participants,
                            participation_requests=participation_requests)

@app.route("/new_participant", methods=["POST"])
def new_participant():
    require_login()
    check_csrf()

    project_id = request.form["project_id"]
    project = projects.get_project(project_id)
    if not project:
        abort(404)

    user_id = session["user_id"]

    if project["user_id"] == user_id:
        abort(403)

    projects.add_participation_request(project_id, user_id)

    return redirect("/project/" + str(project_id))

@app.route("/new_project")
def new_project():
    require_login()

    dance_styles = projects.get_dance_styles()
    levels = projects.get_levels()
    locations = projects.get_locations()

    filled = {
        "title": "",
        "description": "",
        "dance_style_id": "",
        "level_id": "",
        "location_ids": []
        }

    return render_template(
        "new_project.html",
        filled=filled,
        dance_styles=dance_styles,
        levels=levels,
        locations=locations
        )

@app.route("/create_project", methods=["POST"])
def create_project():
    require_login()
    check_csrf()

    dance_styles = projects.get_dance_styles()
    levels = projects.get_levels()
    locations = projects.get_locations()

    title = request.form["title"]
    description = request.form["description"]
    dance_style_id = request.form["dance_style"]
    level_id = request.form["level"]
    location_ids = request.form.getlist("locations")

    filled = {
        "title": title,
        "description": description,
        "dance_style_id": dance_style_id,
        "level_id": level_id,
        "location_ids": location_ids
    }

    errors = []

    if len(title) > 50:
        errors.append("Otsikko saa olla enintään 50 merkkiä pitkä")

    if len(title) < 3:
        errors.append("Otsikon täytyy olla vähintään 3 merkkiä pitkä")

    if len(description) > 1000:
        errors.append("Kuvaus saa olla enintään 1000 merkkiä pitkä")

    if len(description) < 3:
        errors.append("Kuvauksen täytyy olla vähintään 3 merkkiä pitkä")

    if not level_id:
        errors.append("Valitse taso")

    if not location_ids:
        errors.append("Valitse vähintään yksi sijainti")

    if errors:
        for error in errors:
            flash(error)

        return render_template(
            "new_project.html",
            filled=filled,
            dance_styles=dance_styles,
            levels=levels,
            locations=locations
        )

    user_id = session["user_id"]

    projects.add_project(title, description, dance_style_id, level_id, location_ids, user_id)

    return redirect("/")

@app.route("/edit_project/<int:project_id>")
def edit_project(project_id):
    require_login()

    project = projects.get_project(project_id)
    if not project:
        abort(404)

    dance_styles = projects.get_dance_styles()
    levels = projects.get_levels()
    locations = projects.get_locations()

    project_locations = projects.get_project_locations(project_id)
    project_location_ids = [location["id"] for location in project_locations]

    if project["user_id"] != session["user_id"]:
        abort(403)

    filled = {
        "title": project["title"],
        "description": project["description"],
        "dance_style_id": project["dance_style_id"],
        "level_id": project["level_id"],
        "location_ids": project_location_ids
    }

    return render_template("edit_project.html",
                            project=project,
                            filled=filled,
                            dance_styles=dance_styles,
                            levels=levels,
                            locations=locations)

@app.route("/update_project", methods=["POST"])
def update_project():
    require_login()
    check_csrf()

    project_id = request.form["project_id"]

    project = projects.get_project(project_id)
    if not project:
        abort(404)

    if project["user_id"] != session["user_id"]:
        abort(403)

    dance_styles = projects.get_dance_styles()
    levels = projects.get_levels()
    locations = projects.get_locations()

    title = request.form["title"]
    description = request.form["description"]
    dance_style_id = request.form["dance_style"]
    level_id = request.form["level"]
    location_ids = request.form.getlist("locations")

    filled = {
        "title": title,
        "description": description,
        "dance_style_id": dance_style_id,
        "level_id": level_id,
        "location_ids": location_ids
    }

    errors = []

    if len(title) > 50:
        errors.append("Otsikko saa olla enintään 50 merkkiä pitkä")

    if len(title) < 3:
        errors.append("Otsikon täytyy olla vähintään 3 merkkiä pitkä")

    if len(description) > 1000:
        errors.append("Kuvaus saa olla enintään 1000 merkkiä pitkä")

    if len(description) < 3:
        errors.append("Kuvauksen täytyy olla vähintään 3 merkkiä pitkä")

    if not level_id:
        errors.append("Valitse taso")

    if not location_ids:
        errors.append("Valitse vähintään yksi sijainti")

    if errors:
        for error in errors:
            flash(error)

        return render_template(
            "edit_project.html",
            project=project,
            filled=filled,
            dance_styles=dance_styles,
            levels=levels,
            locations=locations
        )

    projects.update_project(
        project_id,
        title,
        description,
        dance_style_id,
        level_id,
        location_ids
    )

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
    filled = {
        "username": ""}
    return render_template("register.html", filled=filled)

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    errors = []

    if len(username) < 3:
        errors.append("Käyttäjänimen täytyy olla vähintään 3 merkkiä pitkä")

    if " " in username:
        errors.append("Käyttäjänimessä ei saa olla välilyöntejä")

    if len(password1) < 6:
        errors.append("Salasanan täytyy olla vähintään 6 merkkiä pitkä")

    if password1 != password2:
        errors.append("Salasanat eivät täsmää")

    if errors:
        for error in errors:
            flash(error)

        filled = {
            "username": username
        }

        return render_template(
            "register.html",
            filled=filled
        )

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        flash("Tunnus on jo varattu")

        filled = {
            "username": username
        }

        return render_template(
            "register.html",
            filled=filled
        )

    filled = {
        "username": username
    }

    return render_template(
        "login.html",
        message="Tunnus luotu onnistuneesti.",
        filled=filled
    )

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        filled = {
            "username": ""}
        return render_template("login.html", filled=filled)

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
            flash("Väärä käyttäjätunnus tai salasana")

            filled = {
                "username": username}

            return render_template("login.html", filled=filled)

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
        del session["csrf_token"]
    return redirect("/")

@app.route("/handle_request", methods=["POST"])
def handle_request():
    require_login()
    check_csrf()

    request_id = request.form["request_id"]
    action = request.form["action"]

    participation_request = projects.get_participation_request(request_id)

    if not participation_request:
        abort(404)

    project = projects.get_project(participation_request["project_id"])

    if project["user_id"] != session["user_id"]:
        abort(403)

    if action == "Hyväksy":
        projects.accept_participation_request(request_id)

    elif action == "Hylkää":
        projects.reject_participation_request(request_id)

    else:
        abort(400)

    return redirect("/project/" + str(project["id"]))