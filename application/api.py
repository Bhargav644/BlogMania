from werkzeug.exceptions import HTTPException, NotFound
from flask_restful import Resource, Api, fields, marshal_with, reqparse
from flask import make_response
from application.models import Users, Blogs, Followers
from flask_security import current_user
from sqlalchemy import or_, and_
from application.db_init import db
user_fields = {
    "id": fields.Integer,
    "username": fields.String,
    "email": fields.String,
    "password": fields.String,
    "active": fields.String,
    "roles": fields.String,
    "profile": fields.String,
    "notifications": fields.String
}
blog_fields = {
    "id": fields.Integer,
    "title": fields.String,
    "author_id": fields.Integer,
    "description": fields.String,
    "imageURL": fields.String,
    "timestamp": fields.String,
    "claps": fields.Integer,
    "private": fields.Integer
}

followers_fields = {
    "id": fields.Integer,
    "username": fields.String,
    "email": fields.String,
    "profile": fields.String,
}

notification_fields = {
    "notifications": fields.String
}


class NotFoundError(HTTPException):
    def __init__(self, status_code, message=''):
        self.response = make_response(message, status_code)


class UsersApi(Resource):
    @ marshal_with(user_fields)
    def get(self, username):
        # Get the user details from the database
        users = Users.query.filter(Users.username == username).scalar()

        if users:
            # user exists in database, hence return the user object which will be marshalled to json
            return users
        else:
            # Return 404 Error
            raise NotFoundError(status_code=404)

    def get_username_by_id(self, user_id):
        username = Users.query.with_entities(
            Users.username).filter(Users.id == user_id).first()
        return username

    def get_id_by_username(self, username):
        userid = Users.query.with_entities(
            Users.id).filter(Users.username == username).first()
        return userid


class BlogsApi(Resource):
    @ marshal_with(blog_fields)
    def get(self, author_id, private=False):

        blog = []
        if private and author_id == current_user.id:
            blogs = Blogs.query.filter(
                Blogs.author_id == author_id).order_by(Blogs.timestamp.desc()).all()
        else:
            blogs = Blogs.query.filter(
                Blogs.author_id == author_id).filter(Blogs.private != 1).order_by(Blogs.timestamp.desc()).all()

        return blogs

    @marshal_with(blog_fields)
    def get_blogs_by_id(self, blog_id, author_id):
        blog = []
        if author_id == current_user.id:
            blogs = Blogs.query.filter(
                Blogs.author_id == author_id).filter(Blogs.id == blog_id).first()

        isPrivate = True if Blogs.query.filter(Blogs.id == blog_id).filter(
            Blogs.private == 1).first() else False

        return (blogs, isPrivate)

    @ marshal_with(blog_fields)
    def get_by_followers(self, followers):

        blogs = Blogs.query.filter(
            or_(Blogs.author_id.in_(
                followers), Blogs.author_id == current_user.id)).filter_by(private=0).order_by(Blogs.timestamp.desc()).all()

        return blogs

    @ marshal_with(blog_fields)
    def get_all(self):

        blogs = Blogs.query.filter(Blogs.private != 1).order_by(
            Blogs.timestamp.desc()).all()
        return blogs

    def count_my_post(self, user_id):
        total_blogs = 0
        if (current_user.id == user_id):
            total_blogs = Blogs.query.filter(
                Blogs.author_id == user_id).count()
        else:
            total_blogs = Blogs.query.filter(
                Blogs.author_id == user_id).filter(Blogs.private != 1).count()
        return total_blogs


class FollowersApi(Resource):

    def get_followers(self, user_id):
        return Followers.query.filter(Followers.user_id == user_id).count()

    def follow(self, user_id):
        return Followers.query.filter(Followers.follower_id == user_id).count()

    @marshal_with(followers_fields)
    def get_followers_with_name(self, user_id):
        followers = db.session.query(Users, Followers).with_entities(Users.id, Users.username, Users.email, Users.profile).filter(
            Followers.user_id == user_id).filter(Followers.follower_id == Users.id).all()
        return followers

    @marshal_with(followers_fields)
    def get_following_with_name(self, user_id):
        following = db.session.query(Users, Followers).with_entities(Users.id, Users.username, Users.email, Users.profile).filter(
            Followers.follower_id == user_id).filter(Followers.user_id == Users.id).all()
        return following


class NotificationsApi(Resource):

    @marshal_with(notification_fields)
    def get_notifications(self, user_id):
        notifications = Users.query.filter(Users.id == user_id).first()
        return notifications
