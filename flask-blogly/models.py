"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import datetime


db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):

     
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String, default= "https://icon-library.com/images/generic-user-icon/generic-user-icon-19.jpg")

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    def __repr__(self):
        u = self
        return f"user {u.id} {u.first_name} {u.last_name} "
    
    def modify_user(self, first_name=None, last_name=None, image_url="https://icon-library.com/images/generic-user-icon/generic-user-icon-19.jpg"):
        if(first_name):
            self.first_name = first_name
        if(last_name):
            self.last_name = last_name
        
        self.image_url = image_url
        return self

    @classmethod
    def get_user_by_id(cls, id):

        return cls.query.filter_by(id=f"{id}").first()
    
     


class Post(db.Model):

    __tablename__ = "posts"


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default= datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"),  nullable=False)

    
    

    def __repr__(self):
        p = self
        return f"user {p.id} {p.title} {p.content} {p.created_at} "

    @classmethod
    def get_posts_by_user(cls, id):
        posts = cls.query.filter_by(user_id=id)
        return posts
    
    @classmethod
    def get_post_by_id(cls, id):
        post = cls.query.filter_by(id=id).first()
        return post
    
    def modify_post(self, title=None, content=""):
        if (title):
            self.title = title
        self.content = content
        return self

    def get_tags_by_post(self):
        tags = self.tags
        return tags

class Tag(db.Model):

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship(
        'Post',
        secondary="post_tags",
        cascade="all,delete",
        backref="tags",
    )

    def __repr__(self):
        t = self
        return f" {t.id} {t.name}"

    @classmethod
    def get_tag_by_id(cls, id):
        id = int(id)
        tag = cls.query.filter_by(id=id).first()
        return tag

    


    @classmethod
    def get_tags(cls):
        tags = cls.query.all()
        return tags

    def get_associated_posts(self):
        posts = self.posts 
        return posts
    def modify_tag(self, name):
    
        if (name is None):
            return False
        self.name = name
        return self



class PostTag(db.Model):

    __tablename__ = "post_tags"

    post_id = db.Column(db.Integer,db.ForeignKey("posts.id"), primary_key=True )
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True )

    # tags = db.relationship("Tag", backref="posts_tags")

   