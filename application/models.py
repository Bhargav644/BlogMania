from flask_security import UserMixin, RoleMixin
from application.db_init import db


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(),
                                 db.ForeignKey('users.id')),
                       db.Column('role_id', db.Integer(),
                                 db.ForeignKey('role.id'))
                       )


class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    profile = db.Column(db.String(80), nullable=True)
    notifications = db.Column(db.String(80))


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class Blogs(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(80))
    author_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False)
    description = db.Column(db.String(80))
    imageURL = db.Column(db.String(80))
    timestamp = db.Column(db.String(80))
    private = db.Column(db.Boolean(), default=False)


class BlogClaps(db.Model):
    __tablename__ = 'blogclaps'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )
    blog_id = db.Column(
        db.Integer, db.ForeignKey("blogs.id"), nullable=False
    )


class Followers(db.Model):
    __tablename__ = 'followers'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )
    follower_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )
