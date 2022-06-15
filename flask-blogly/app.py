"""Blogly application."""

from flask import Flask, request, redirect, render_template, session, flash
from models import db, connect_db, User

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
    return render_template('user_details.html', user=user)

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
    print("*******",img)
    user = User.get_user_by_id(user_id)
    modified_user = user.modify_user(first, last, img)

    db.session.add(modified_user)
    db.session.commit()


    return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    user = User.get_user_by_id(user_id)

    User.query.filter(User.id == user_id).delete()
    db.session.commit()
    return redirect("/users")


def valid_name(name):
    if (name == " "):
            flash('Neither first nor last name can be just a space')
            return False
    else:
         return True