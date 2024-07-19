"""Create page."""
import flask
import insta485


@insta485.app.route('/accounts/create/')
def show_create():
    """Create page."""
    if 'username' not in flask.session:
        return flask.render_template('create.html')
    target_url = flask.request.args.get('/accounts/edit/')
    return flask.redirect(target_url)
