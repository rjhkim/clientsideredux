"""Delete page."""
import flask
import insta485


@insta485.app.route('/accounts/delete/')
def show_delete():
    """Delete page."""
    if 'username' not in flask.session:
        return flask.redirect("/accounts/login/")
    logname = flask.session['username']
    context = {"logname": logname}
    return flask.render_template('delete.html', **context)
