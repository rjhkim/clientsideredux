"""
Insta485 index (main) view.

URLs include:
/
"""
import os
import flask
import insta485


app = flask.Flask(__name__)


insta485.app.secret_key = os.urandom(24)


@insta485.app.route('/accounts/auth/')
def auth():
    """Authorize page."""
    if 'username' in flask.session:
        return ('', 200)
    flask.abort(403)
