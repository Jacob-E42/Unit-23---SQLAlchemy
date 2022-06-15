from flask import Flask, request, redirect, render_template, session, flash
from models import db, connect_db, User
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from unittest import TestCase
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class FlaskTests(TestCase):

    def setUp(self):
        User.query.delete()
        db.session.commit()
        fred = User(id = 17,first_name="Fred", last_name="whynot")
        db.session.add(fred)
        db.session.commit()
       
    def tearDown(self):
        db.session.rollback()
        User.query.filter_by(id="1").delete()
        db.session.commit()

    def test_show_new_user_form(self):
        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Enter a First Name', html)
    def test_submit_new_user(self):
        with app.test_client() as client:
            resp = client.post("/users/new", data={"first_name": "John","last_name": "Fresson", 'img': "None"}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('John Fresson', html)
    def test_user_details(self):
        with app.test_client() as client:
            resp = client.get("/users/17")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Fred whynot', html)
    def test_edit_page(self):
        with app.test_client() as client:
            resp = client.get("/users/17/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Fred', html)
            self.assertIn('Edit a User', html)


