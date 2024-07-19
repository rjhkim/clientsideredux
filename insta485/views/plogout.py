"""Account logout page."""
import flask
from flask import session
import insta485


@insta485.app.route('/accounts/logout/', methods=['POST'])
def logout_post():
    """Account logout page."""
    if 'username' not in flask.session:
        return flask.redirect("/accounts/login/")
    session.pop('username', None)
    target_url = flask.request.args.get('target', '/accounts/login/')
    return flask.redirect(target_url)
