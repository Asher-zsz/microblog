from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index = True, unique=True)
    email = db.Column(db.String(120), index = True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic') # for "one-to-many" cases, the relationship field normally defined on "one" side
    # backref='author' means to add a 'author' field to Post, and can be used like this：
    # >>> u = User.query.get(1)
    # >>> p = Post(body='my first post!', author=u)


    def __rep__(self):
        return '<User {}>'.format(self.username) # the representation when printing

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # lower case of user, which represents the data table of the model

    def __rep__(self):
        return '<Post {}>'.format(self.body)