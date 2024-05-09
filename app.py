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

# the list of users
@app.route("/")
def home():
    users = User.query.all()
    return render_template("users.html", users=users)

#list of users post
@app.route("/", methods=["POST"])
def user_post():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url= request.form["image_url"]

    new_user = User(first_name=first_name,last_name=last_name,image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/')
# the user details page
@app.route('/<int:id>')
def user_details(id):
    user = User.query.get_or_404(id)
    return render_template("details.html", user=user)

# form
@app.route("/users/new")
def add_user():
    return render_template("form.html")

# edit
@app.route("/edit")
def edit_user():
    return render_template("edit.html")

# delete
@app.route("/users/<int:id>/delete", methods=["POST"])
def users_destroy(id):

    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/")

# user posts form
@app.route("/users/<int:id>/posts/new")
def add_post_form(id):
    # Assuming you have a way to fetch the user object by ID
    user = User.query.get(id)
    return render_template("add_post.html", user=user)

# user form redirect to details page

@app.route('/<int:id>', methods=["POST"])
def post_title(id):

    user = User.query.get(id)
    title = request.form["title"]
    content = request.form["content"]

    new_post = Post(title=title, content=content, user_id=id)  # Associate post with user

    db.session.add(new_post)
    db.session.commit()

    return render_template("details.html", user=user, new_post=new_post)
