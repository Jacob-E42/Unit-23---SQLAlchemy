"""Blogly application."""

from flask import Flask, request, redirect, render_template, session, flash
from models import db, connect_db, User, Post


from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'Nope'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()



@app.route('/')
def show_homepage():

    return redirect("/users")

@app.route('/users')
def show_users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new')
def show_add_form():
    return render_template('new_user_form.html')

@app.route('/users/new', methods=["POST"])
def process_add_user_form():
    first = request.form['first_name']
    last = request.form['last_name']
    img = request.form["img"] 
    if (not valid_name(first)):
        return redirect("/users/new")
    if (not valid_name(last)):
        return redirect("/users/new")
    img = img if img else None
    new_user = User(first_name=first, last_name=last , image_url=img)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user_info(user_id):
    user = User.get_user_by_id(user_id)
    posts = Post.get_posts_by_user(user_id)
    
    return render_template('user_details.html', user=user, posts=posts)

@app.route('/users/<int:user_id>/edit')
def show_edit_page(user_id):
    user = User.get_user_by_id(user_id)
    return render_template("edit_user.html", user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def process_edit_page(user_id):
    first = request.form['first_name']
    last = request.form['last_name']
    img = request.form["img"]
    if (not valid_name(first)):
        print('here i am')
        return redirect(f"/users/{user_id}/edit")
    if (not valid_name(last)):
        print('here i am')

        return redirect(f"/users/{user.id}/edit")
    img = img if img else None
    
    user = User.get_user_by_id(user_id)
    modified_user = user.modify_user(first, last, img)

    db.session.add(modified_user)
    db.session.commit()


    return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    user = User.get_user_by_id(user_id)

    db.session.delete(user)
    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:user_id>/posts/new")
def show_new_post_form(user_id):
    user = User.get_user_by_id(user_id)
    return render_template("new_post_form.html", user=user) 

@app.route("/users/<int:user_id>/posts/new", methods=['POST'])
def add_new_post(user_id):
    title = request.form["title"]
    content = request.form["content"]
    new_post = Post(title=title, content=content, user_id=user_id)


    db.session.add(new_post)
    db.session.commit()
    return redirect(f"/users/{user_id}") 


################################################# Post Routes
@app.route("/posts/<int:post_id>")
def show_post(post_id):
    post = Post.get_post_by_id(post_id)
    return render_template("post_details.html", post=post) 

@app.route("/posts/<int:post_id>/edit")
def edit_post_form(post_id):
    post = Post.get_post_by_id(post_id)
    return render_template("edit_post.html", post=post) 

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    title = request.form['title']
    content =  request.form['content']
    post = Post.get_post_by_id(post_id)
    modified_post = post.modify_post(title, content)
    print(modified_post, "*********")
    db.session.add(modified_post)
    db.session.commit()
    return redirect(f"/posts/{post_id}") 

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = Post.get_post_by_id(post_id)
    user_id = post.user_id
    user = User.get_user_by_id(user_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f"/users/{user_id}") 






def valid_name(name):
    if (name == " "):
            flash('Neither first nor last name can be just a space')
            return False
    else:
         return True