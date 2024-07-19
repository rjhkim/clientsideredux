"""Login page."""
import flask
import insta485


@insta485.app.route('/accounts/login/')
def show_login():
    """Login page."""
    if 'username' not in flask.session:
        return flask.render_template('login.html')
    return flask.redirect('/')
