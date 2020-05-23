from flask_sqlalchemy import SQLAlchemy
from app import db
#Instead of including foriegn key, we use login manager to find current user and then have current username dumped into database
#Will do it tomorrow
class Todo(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    text = db.Column(db.String(200) , nullable = 'False')
    desc = db.Column(db.String(400))
    deadline = db.Column(db.String(24) , nullable = 'False')
    complete = db.Column(db.Boolean)

class User(db.Model):
    __bind_key__ = 'user'
    id = db.Column(db.Integer , primary_key=True)
    email = db.Column(db.String() , nullable = False , unique=True)
    username = db.Column(db.String(120) , nullable = False , unique=True)
    password = db.Column(db.String(120) , nullable = False)
    firstname = db.Column(db.String(120) , nullable = False)
    lastname = db.Column(db.String(120) , nullable = False)

    def is_active(self):
       return True
