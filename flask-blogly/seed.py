from models import User, db, Post, Tag
from app import app


db.drop_all()
db.create_all()

User.query.delete()
Post.query.delete()
Tag.query.delete()


emily = User(first_name="Emily", last_name="Blank")
fred = User(first_name="Fred", last_name="Someone")
george = User(first_name="George", last_name="Person")


db.session.add(emily)
db.session.add(fred)
db.session.add(george)

db.session.commit()


post1 = Post(title="today's weather", content="looking pretty sunny", user_id=1)
post2 = Post(title="Ambitions", content="I think I'm going to build a castle today", user_id= 2)
post3 = Post(title="Biology", content="The immune system has a special organ that tests if potential antibodies will be harmful to the body.", user_id= 3)

db.session.add(post1)
db.session.add(post2)
db.session.add(post3)

db.session.commit()

tag1 = Tag(name="culture")
tag2 = Tag(name="science")
tag3 = Tag(name="politics")

db.session.add(tag1)
db.session.add(tag2)
db.session.add(tag3)

db.session.commit()

post1.tags.append(tag1)
post2.tags.append(tag3)
post2.tags.append(tag1)
post3.tags.append(tag2)

db.session.commit()