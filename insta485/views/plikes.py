import flask
import insta485
import arrow
from flask import send_from_directory


@insta485.app.route('/likes/', methods=['POST'])
def like_post():
    if 'username' not in flask.session:
        return flask.redirect("/accounts/login/")
    logname = flask.session['username']

    connection = insta485.model.get_db()
    operation = flask.request.form['operation']
    postid = flask.request.form['postid']


    if operation == 'like':
        # Check if the user has already liked the post 
        cur = connection.execute(
            "SELECT * FROM likes WHERE owner = ? AND postid = ?",
            (logname, postid)
        )
        existing_like = cur.fetchone()
        if existing_like:
            # The user has already liked this post
            flask.abort(409)
        else:
            # Insert a new like for the post
            connection.execute(
                "INSERT INTO likes (owner, postid) VALUES (?, ?)",
                (logname, postid)
            )
            # Commit the transaction (important!)
            connection.commit()

    elif operation == 'unlike':
        # Check if the user has already liked the post
        cur = connection.execute(
            "SELECT * FROM likes WHERE owner = ? AND postid = ?",
            (logname, postid)
        )
        existing_like = cur.fetchone()
        if existing_like:
            # Remove the like for the post
            connection.execute(
                "DELETE FROM likes WHERE owner = ? AND postid = ?",
                (logname, postid)
            )
            # Commit the transaction (important!)
            connection.commit()
        else:
            # The user has not liked this post
            flask.abort(409)
    # Redirect back to the target URL
    target_url = flask.request.args.get('target', '/')
    return flask.redirect(target_url)
        