from flask import Flask, request, redirect, render_template, session, flash
from models import db, connect_db, User, Post
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
        Post.query.delete()
        User.query.delete()
        
        fred = User(id=17, first_name="Fred", last_name="Someone")
        db.session.add(fred)
        db.session.commit()
        
        
        post1 = Post(id=1, title="today's weather", content="looking pretty sunny", user_id=17)
        db.session.add(post1)
        db.session.commit()
        
       
    def tearDown(self):
        
       
        db.session.rollback()
        
        

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
            self.assertIn('Fred Someone', html)
    def test_edit_page(self):
        with app.test_client() as client:
            
            resp = client.get("/users/17/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Fred', html)
            self.assertIn('Edit a User', html)
    def test_new_post(self):
        with app.test_client() as client:
            
            resp = client.get("/users/17/posts/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('New Post for Fred', html)

    def test_post_details(self):
        with app.test_client() as client:
            
            resp = client.get("/posts/1")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('looking pretty sun', html)

    def test_edit_post(self):
        def test_post_details(self):
            with app.test_client() as client:
                
                resp = client.get("/posts/1/edit")
                html = resp.get_data(as_text=True)

                self.assertEqual(resp.status_code, 200)
                self.assertIn("today's weather", html)


