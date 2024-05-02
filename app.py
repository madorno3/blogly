from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.app_context().push()

connect_db(app)
db.create_all()

@app.route("/")
def home():
    users = User.query.all()
    return render_template("users.html", users=users)

@app.route("/", methods=["POST"])
def user_post():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url= request.form["image_url"]

    new_user = User(first_name=first_name,last_name=last_name,image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/')

@app.route('/<int:id>')
def user_details(id):
    user = User.query.get_or_404(id)
    return render_template("details.html", user=user)

@app.route("/users/new")
def add_user():
    return render_template("form.html")

@app.route("/edit")
def edit_user():
    return render_template("edit.html")

@app.route("/users/<int:id>/delete", methods=["POST"])
def users_destroy(id):

    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/")


