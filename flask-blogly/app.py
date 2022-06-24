"""Blogly application.

app.py defines endroutes for a lightweight flask blogging app. There is functionality for 
CRUD operations for users, posts and blog tags. 
"""

from flask import Flask, request, redirect, render_template, session, flash
from models import db, connect_db, User, Post, Tag


from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'Nope'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

#connects db and creates all tables on the db server
connect_db(app)
db.create_all()


#No homepage, instead redirects to user list
@app.route('/')
def show_homepage():

    return redirect("/users")

@app.route('/users')
def show_users():
    """Display a list of all users on the app"""

    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new')
def show_add_form():
    """Show a form for creating a new user"""

    return render_template('new_user_form.html')

@app.route('/users/new', methods=["POST"])
def process_add_user_form():
    """Process a new user and add their info to the db"""

    first = request.form['first_name']
    last = request.form['last_name']
    img = request.form["img"] or None

    
    # img = img if img else None

    new_user = User(first_name=first, last_name=last , image_url=img)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user_info(user_id):
    """Show the details for a given user, and their posts."""

    user = User.query.get_or_404(user_id)
    posts = Post.get_posts_by_user(user_id)
    
    return render_template('user_details.html', user=user, posts=posts)

@app.route('/users/<int:user_id>/edit')
def show_edit_page(user_id):
    """"Show the edit form for a given user"""

    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def process_edit_page(user_id):
    """Process the edited info for a user and update the db"""

    first = request.form['first_name']
    last = request.form['last_name']
    img = request.form["img"] or None

    

    # img = img if img else None
    
    user = User.query.get_or_404(user_id)
    modified_user = user.modify_user(first, last, img)

    db.session.add(modified_user)
    db.session.commit()


    return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete a user from the db."""

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()
    return redirect("/users")




################################################# Post Routes
@app.route("/users/<int:user_id>/posts/new")
def show_new_post_form(user_id):
    """Show a form to create a new post for a given user."""

    user = User.query.get_or_404(user_id)
    tags = Tag.get_tags()
    return render_template("new_post_form.html", user=user, tags=tags) 

@app.route("/users/<int:user_id>/posts/new", methods=['POST'])
def add_new_post(user_id):
    """Process new post and add it to posts table in db"""

    title = request.form["title"]
    content = request.form["content"]
    
    new_post = Post(title=title, content=content, user_id=user_id)
    
    db.session.add(new_post)
    tag_ids = request.form.getlist("tags")
    
    if (tag_ids is not None):
        for id in tag_ids:
            tag = Tag.query.get_or_404(id)
            new_post.tags.append(tag)

    db.session.commit()
    return redirect(f"/users/{user_id}") 

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Show details page for a post."""

    post = Post.query.get_or_404(post_id)
    tags = post.get_tags_by_post()
    return render_template("post_details.html", post=post, tags=tags) 

@app.route("/posts/<int:post_id>/edit")
def edit_post_form(post_id):
    """Show edit form for a post"""

    post = Post.query.get_or_404(post_id)
    tags = Tag.get_tags()
    return render_template("edit_post.html", post=post, tags=tags) 

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    """Process new post info and add to db"""

    title = request.form['title']
    content =  request.form['content']
    post = Post.query.get_or_404(post_id)
    modified_post = post.modify_post(title, content)
    
    db.session.add(modified_post)
    tag_ids = request.form.getlist("tags")
    
    if (tag_ids is not None):
        for id in tag_ids:
            tag = Tag.query.get_or_404(id)
            modified_post.tags.append(tag)
    db.session.commit()
    return redirect(f"/posts/{post_id}") 

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Delete a given post from the db"""

    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    
    db.session.delete(post)
    db.session.commit()
    return redirect(f"/users/{post.user_id}") 


######################################################### Tag Routes

@app.route("/tags")
def show_tags_list():
    """Show all tags that have been created on the app."""

    tags = Tag.get_tags()
    
    return render_template("tags_list.html", tags=tags)

@app.route("/tags/<int:tag_id>")
def show_tag_details(tag_id):
    """Show details page for a tag, which dispays links to articles which use this tag."""

    tag = Tag.query.get_or_404(tag_id)
    posts = tag.get_associated_posts()
    return render_template("tag_details.html", tag=tag, posts=posts)

@app.route("/tags/new")
def create_tag():
    """Show form to make a new tag."""

    return render_template("create_tag.html")

@app.route("/tags/new", methods=["POST"])
def post_new_tag():
    """Add new tag to tags table in db."""

    name = request.form["name"]
    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()
    
    return redirect("/tags")

@app.route("/tags/<int:tag_id>/edit")
def edit_tag(tag_id):
    """Show form to edit a tag's info."""

    tag = Tag.query.get_or_404(tag_id)
    return render_template("edit_tag.html", tag=tag)

@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def post_edited_tag(tag_id):
    """Update db with the edited tag info."""
    name = request.form["name"]
    tag = Tag.query.get_or_404(tag_id)

    modified_tag = tag.modify_tag(name)
    db.session.add(modified_tag)
    db.session.commit()

    return redirect("/tags")

@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """Delete a given tag from db."""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")



