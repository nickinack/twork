from flask_sqlalchemy import SQLAlchemy, event
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(24), nullable=False)
    lastname = db.Column(db.String(24))
    username = db.Column(db.String(24), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)


@event.listens_for(User.password, 'set', retval=True)
def hash_user_password(target, value, oldvalue, initiator):
    if value != oldvalue:
        return generate_password_hash(value)
    return value


class todo(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    text = db.Column(db.String(200))
    desc = db.Column(db.String(400))
    deadline = db.Column(db.Date)
    complete = db.Column(db.Boolean)

