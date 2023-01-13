
''' Importing Important Libraries '''
from application.controllers import Routes
from flask import Flask, render_template, request, jsonify
from application.db_init import db
from flask_security import Security, SQLAlchemySessionUserDatastore
from application.models import Users, Role
from application.config import Config
from application.flaskSecurity import ExtendedRegisterForm
import json
from flask_restful import Api
from application.api import BlogsApi, UsersApi, FollowersApi, NotificationsApi


''' Initializing Flask App Here '''
app = None
api = None


def create_app():
    app = Flask(__name__)

    ''' Connecting Database With App '''
    app.config.from_object(Config)
    db.init_app(app)

    ''' This will make current_app point at this application '''
    app.app_context().push()
    # db.create_all()

    ''' Letting Know Flask Security Regarding Our Data'''
    user_datastore = SQLAlchemySessionUserDatastore(db.session, Users, Role)

    ''' Setting Up Username in Registration Form '''

    sec = Security(app, user_datastore,
                   register_form=ExtendedRegisterForm)
    api = Api(app)
    api.add_resource(BlogsApi, "/blog/details/api/<int:author_id>",)
    api.add_resource(UsersApi, "/users/details/api/<username>",)
    return app


app = create_app()


''' Import All The Routes To app.py'''
Routes()


@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html")


if __name__ == '__main__':
    app.run(debug=True)
