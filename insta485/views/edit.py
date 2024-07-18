import flask
import insta485
import arrow
from flask import send_from_directory


@insta485.app.route('/accounts/edit/')
def show_edit():
    if 'username' not in flask.session:
        return flask.redirect("/accounts/login/")
    logname = flask.session['username']

    connection = insta485.model.get_db()
    pic = connection.execute(
        "SELECT users.filename, users.fullname, users.email "
        "FROM users WHERE users.username = ?", (logname, ))
    profile = pic.fetchone()
    context = {
       "logname": logname,
       "profile": profile
    }
    return flask.render_template('edit.html', **context)
