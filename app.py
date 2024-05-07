from datetime import datetime
from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post
from flask import url_for


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

@app.route("/users/<int:id>/posts/new")
def add_post_form(id):
    # Assuming you have a way to fetch the user object by ID
    user = User.query.get(id)
    return render_template("add_post.html", user=user)

@app.route("/users/<int:id>/posts/new", methods=["POST"])
def save_post(id):
    # Assuming you have a way to fetch the user object by ID
    
    user = User.query.get(id)
    new_post = Post(title=request.form['title'],content=request.form['content'],user=user)
    db.session.add(new_post)
    db.session.commit()

    return redirect("<int:id>'")

# @app.route("/posts/<int:post_id>")
# def show_posts(post_id):
#     post = Post.query.get_or_404(post_id)
#     return render_template("show.html", post=post)



