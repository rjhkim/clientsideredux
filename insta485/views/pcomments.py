import flask
import insta485
import arrow
from flask import send_from_directory


@insta485.app.route('/comments/', methods=['POST'])
def comment_post():
    if 'username' not in flask.session:
        return flask.redirect("/accounts/login/")
    logname = flask.session['username']

    connection = insta485.model.get_db()
    operation = flask.request.form['operation']
    #handle cases where user tries to create empty comment
    #handle cases where user tries to delete a comment that they do not own


    if operation == 'create':
        postid = flask.request.form['postid']
        text = flask.request.form['text']
        # Check if user tries to create an empty comment
        if text:
            # Insert a new comment for the post
            connection.execute(
                "INSERT INTO comments (owner, postid, text) VALUES (?, ?, ?)",
                (logname, postid, text)
            )
            # Commit the transaction (important!)
            connection.commit()
        
        else:
            # User tries to submit an empty comment
            flask.abort(400)

    elif operation == 'delete':
        commentid = flask.request.form['commentid']

        # Check if the user owns this comment
        cur = connection.execute(
            "SELECT * FROM comments WHERE owner = ? AND commentid = ?",
            (logname, commentid)
        )
        existing_comment = cur.fetchone()
        if existing_comment:
            # Remove the comment for this post
            connection.execute(
                "DELETE FROM comments WHERE owner = ? AND commentid = ?",
                (logname, commentid)
            )
            # Commit the transaction (important!)
            connection.commit()
        else:
            # The user does not own this comment
            flask.abort(403)
    # Redirect back to the target URL
    target_url = flask.request.args.get('target', '/')
    return flask.redirect(target_url)
        