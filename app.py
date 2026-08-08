import sqlite3
from flask import Flask
from flask import redirect, abort, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import db
import config
import projects


app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    all_projects = projects.get_projects()
    return render_template("index.html", projects=all_projects)

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
    return render_template("show_project.html", project=project)

@app.route("/new_project")
def new_project():
    dance_styles = db.query("SELECT * FROM dance_styles")
    return render_template("new_project.html", dance_styles=dance_styles)

@app.route("/create_project", methods=["POST"])
def create_project():
    title = request.form["title"]
    description = request.form["description"]
    dance_style_id = request.form["dance_style"]
    user_id = session["user_id"]

    projects.add_project(title, description, dance_style_id, user_id)

    return redirect("/")

@app.route("/edit_project/<int:project_id>")
def edit_project(project_id):
    project = projects.get_project(project_id)
    dance_styles = db.query("SELECT * FROM dance_styles")
    return render_template("edit_project.html", project=project, dance_styles=dance_styles)

@app.route("/update_project", methods=["POST"])
def update_project():
    project_id = request.form["project_id"]
    title = request.form["title"]
    description = request.form["description"]
    dance_style_id = request.form["dance_style"]

    projects.update_project(project_id, title, description, dance_style_id)

    return redirect("/project/" + str(project_id))

@app.route("/remove_project/<int:project_id>", methods=["GET", "POST"])
def remove_project(project_id):
    if request.method == "GET":
        project = projects.get_project(project_id)
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
        result = db.query(sql, [username])[0]
        user_id = result["id"]
        password_hash = result["password_hash"]


        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")