from datetime import datetime
from app import db, login

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5


# Since this is an auxiliary table that has no data other than the foreign keys, 
# I created it without an associated model class.
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model): # 通过继承UserMixin来继承 is_authenticated, is_active, is_anonymous, get_id()等几个属性与方法
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index = True, unique=True)
    email = db.Column(db.String(120), index = True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic') # for "one-to-many" cases, the relationship field normally defined on "one" side
    # backref是针对右边的entity说的，也就是说，从Post角度看，当需要查询post的作者时，
    # backref='author' means to add a 'author' field to Post, and can be used like this：
    # >>> u = User.query.get(1)
    # >>> p = Post(body='my first post!', author=u)
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id), # c represents Column
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic') # A mode of dynamic sets up the query to not run until specifically requested
        # backref defines how this relationship will be accessed from the right side entity. 
        # From the left side, the relationship is named followed, 
        # so from the right side I am going to use the name followers to represent all the left side users that are linked to the target user in the right side.
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        # the left side foreign key set to the self user, and the right side set to the user argument.
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0 # result：0 or 1
    
    def followed_posts(self):
        followed =  Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())



    # methods to deal with password hash
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __rep__(self): # the representation when printing
        return '<User {}>'.format(self.username) 
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)


class Post(db.Model):
    __searchable__ = ['body'] # this __searchable__ attribute that I added is just a variable, it does not have any behavior associated with it
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # lower case of user, which represents the data table of the model

    def __rep__(self):
        return '<Post {}>'.format(self.body)



@login.user_loader # 可以用来得到current_user
def load_user(id):
    return User.query.get(int(id))