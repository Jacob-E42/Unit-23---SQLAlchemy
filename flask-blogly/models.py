"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

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
    