"""Password page."""
import flask
import insta485


@insta485.app.route('/accounts/password/')
def show_password_page():
    """Password page."""
    if 'username' not in flask.session:
        return flask.redirect("/accounts/login/")
    logname = flask.session['username']

    context = {
       "logname": logname
    }
    return flask.render_template("password.html", **context)
