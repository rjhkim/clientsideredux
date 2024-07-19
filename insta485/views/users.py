"""Username page."""
import flask
import insta485


@insta485.app.route('/users/<username>/')
def get_user(username):
    """Username page."""
    connection = insta485.model.get_db()
    if 'username' not in flask.session:
        return flask.redirect("/accounts/login/")
    logname = flask.session['username']
    # Check if the user exists
    cur_user_check = connection.execute(
        "SELECT 1 FROM users WHERE username = ?",
        (username,)
    )
    user_exists = cur_user_check.fetchone()
    if not user_exists:
        flask.abort(404)
    # post count and the username
    cur1 = connection.execute(
        "SELECT posts.owner as owner, COUNT(*) as post_count, "
        "posts.filename as file, users.fullname as fullname "
        "FROM posts "
        "LEFT JOIN users ON posts.owner = users.username "
        "WHERE posts.owner = ? ",
        (username,)
    )
    post_details = cur1.fetchall()
    cur2 = connection.execute(
        "SELECT following.username1 "
        "FROM following "
        "WHERE username1 = ? AND username2 = ?",
        (logname, username)
    )
    follow_bool = cur2.fetchall()
    cur3 = connection.execute(
        "SELECT DISTINCT COUNT(*) as count "
        "FROM following "
        "WHERE username2 = ? ",
        (username,)
    )
    follower_count = cur3.fetchall()
    cur4 = connection.execute(
        "SELECT DISTINCT COUNT(*) as count "
        "FROM following "
        "WHERE username1 = ? ",
        (username,)
    )
    following_count = cur4.fetchall()
    cur5 = connection.execute(
        "SELECT posts.filename as filename, posts.postid as id "
        "FROM posts "
        "WHERE posts.owner = ? ",
        (username,)
    )
    filename = cur5.fetchall()
    cur6 = connection.execute(
        "SELECT users.fullname as fullname "
        "FROM users "
        "WHERE users.username = ? ",
        (username,)
    )
    fullname = cur6.fetchall()
    context = {
        "post_details": post_details,
        "follow_bool": follow_bool,
        "follower_count": follower_count,
        "following_count": following_count,
        "logname": logname,
        "username": username,
        "fullname": fullname,
        "filename": filename
    }
    return flask.render_template("users.html", **context)
