import flask
import insta485
import arrow
from flask import send_from_directory


@insta485.app.route('/accounts/password/')
def show_password_page():
    logname = "awdeorio"
    context = {
       "logname": logname
    }
    return flask.render_template("password.html", **context)
