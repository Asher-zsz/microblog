from datetime import datetime
from app import db, login

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model): # 通过继承UserMixin来继承 is_authenticated, is_active, is_anonymous, get_id()等几个属性与方法
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index = True, unique=True)
    email = db.Column(db.String(120), index = True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic') # for "one-to-many" cases, the relationship field normally defined on "one" side
    # backref='author' means to add a 'author' field to Post, and can be used like this：
    # >>> u = User.query.get(1)
    # >>> p = Post(body='my first post!', author=u)
    
    # methods to deal with password hash
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __rep__(self): # the representation when printing
        return '<User {}>'.format(self.username) 

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # lower case of user, which represents the data table of the model

    def __rep__(self):
        return '<Post {}>'.format(self.body)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))