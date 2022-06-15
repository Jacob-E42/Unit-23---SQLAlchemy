from models import User, db
from app import app


db.drop_all()
db.create_all()

User.query.delete()


emily = User(first_name="Emily", last_name="Blank")
fred = User(first_name="Fred", last_name="Someone")
george = User(first_name="George", last_name="Person")

db.session.add(george)
db.session.add(emily)
db.session.add(fred)

db.session.commit()