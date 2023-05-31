from app import db, bcrypt, login_manager
from sqlalchemy.sql import func
from flask_login import UserMixin

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.String(1024), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    owner_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    owner = db.relationship('User')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)

    @property
    def passw(self):
        return self.passw
    
    @passw.setter
    def passw(self, plain_text_password):
        self.password = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    
    def check_password(self, entered_password):
        return bcrypt.check_password_hash(self.password, entered_password)


class Vote(db.Model):
    __tablename__ = "votes"

    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    post_id = db.Column(db.Integer(), db.ForeignKey('posts.id', ondelete="CASCADE"), primary_key=True)
