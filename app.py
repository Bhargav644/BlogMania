
''' Importing Important Libraries '''
from application.controllers import Routes
from flask import Flask, render_template, request, jsonify
from application.db_init import db
from flask_security import Security, SQLAlchemySessionUserDatastore
from application.models import Users, Role
from application.config import Config
from application.flaskSecurity import ExtendedRegisterForm
import json

''' Initializing Flask App Here '''
app = None


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
    return app


app = create_app()

''' Import All The Routes To app.py'''
Routes()


@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html")


if __name__ == '__main__':
    app.run(debug=True)
