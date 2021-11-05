from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create_user", methods=["POST"])
def create_users():
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "username": request.form['username'],
        "password": pw_hash
    }
    User.create_user(data)
    return redirect("/")

@app.route('/login_user', methods=['POST'])
def login_user():
    # see if the username provided exists in the database
    data = { "username" : request.form["username"] }
    user_in_db = User.get_by_username(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Username/Password")
        return redirect("/login")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Username/Password")
        return redirect('/login')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name
    session['logged_in'] = True
    # never render on a post!!!
    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    if session.get('logged_in') == "none":
        return redirect("/")
    if not session.get('logged_in') == True:
        return redirect("/")
    id = {"id": session['user_id']}
    return render_template('dashboard.html', users=User.show_user(id), recipes = Recipe.get_recipes(id))

@app.route("/create")
def new_recipe():
    if session.get('logged_in') == "none":
        return redirect("/")
    if not session.get('logged_in') == True:
        return redirect("/")
    return render_template("new_recipe.html")

@app.route("/create_new", methods = ['POST'])
def create_new():
    if not Recipe.validate_recipe(request.form):
        return redirect('/create')
    data = {
        "user_id": session['user_id'],
        "recipe_name": request.form['recipe_name'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "under_30": request.form['under_30'],
        "created_at": request.form['created_at']
    }
    Recipe.create_recipe(data)
    return redirect('/dashboard')

@app.route("/edit/<recipe_id>")
def edit(recipe_id):
    if session.get('logged_in') == "none":
        return redirect("/")
    if not session.get('logged_in') == True:
        return redirect("/")
    data = {
        "id": recipe_id,
        "user_id": session['user_id']
        }
    return render_template('edit_recipe.html', recipe=Recipe.get_one_recipe(data))

@app.route("/recipe/<recipe_id>")
def show_recipe(recipe_id):
    if session.get('logged_in') == "none":
        return redirect("/")
    if not session.get('logged_in') == True:
        return redirect("/")
    data = {
        "id": recipe_id,
        "user_id": session['user_id']
        }
    return render_template("show_recipe.html", recipe=Recipe.get_one_recipe(data))

@app.route("/delete/<recipe_id>")
def delete(recipe_id):
    recipe_id = {"recipe_id": recipe_id}
    Recipe.delete_recipe(recipe_id)
    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')