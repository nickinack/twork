from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):
    # __bind_key__ = 'user'
    id = db.Column(db.Integer , primary_key=True)
    email = db.Column(db.String() , nullable = False , unique=True)
    username = db.Column(db.String(120) , nullable = False , unique=True)
    password = db.Column(db.String(120) , nullable = False)
    firstname = db.Column(db.String(120) , nullable = False)
    lastname = db.Column(db.String(120) , nullable = False)
    todos = db.relationship('Todo', backref='user', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')
    
    def check_password(self, password):
        return check_password(self.password, password)


class Todo(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    text = db.Column(db.String(200) , nullable = 'False')
    desc = db.Column(db.String(400))
    deadline = db.Column(db.String(24) , nullable = 'False')
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
