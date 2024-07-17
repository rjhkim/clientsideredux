import flask
import insta485
import arrow
from flask import send_from_directory
from flask import session


@insta485.app.route('/accounts/logout/', methods=['POST'])
def logout_post():
    logname = "awdeorio"
    session.pop('username', None)
    target_url = flask.request.args.get('target', '/accounts/login/')
    return flask.redirect(target_url)
        