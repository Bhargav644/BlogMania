from flask_security.forms import RegisterForm
from wtforms import StringField
from wtforms.validators import InputRequired


class ExtendedRegisterForm(RegisterForm):
    username = StringField('Username', [InputRequired()])
