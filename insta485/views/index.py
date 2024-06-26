"""
Insta485 index (main) view.

URLs include:
/
"""
import flask
import insta485


@insta485.app.route('/')
def show_index():
    """Display / route."""

    # Connect to database
    connection = insta485.model.get_db()

    # Query database
    # get all posts from logname, also users that logname follow
    # get a container of posts, for each posts their comments
    # For each post:
    # user table: username, filename
    # post table: filename, owner created
    # like table: like count tied to postid as likes
    # comments table: comments
    # like or unlike button
    # comment input button
    # following

    logname = "awdeorio"
    cur = connection.execute(
        "SELECT users.username, users.filename, posts.filename, posts.created, "
        "COUNT(likes), comments.owner, comments.text, "
        "FROM users "
        "INNER JOIN posts"
        "ON posts.owner=users.username"
        "WHERE users.username != ?",
        (logname, )
    )
    users = cur.fetchall()

    # Add database info to context
    context = {"users": users}
    return flask.render_template("index.html", **context)
