"""Post requests for following."""
import flask
import insta485


@insta485.app.route('/following/', methods=['POST'])
def following_post():
    """Post requests for following."""
    if 'username' not in flask.session:
        return flask.redirect("/accounts/login/")
    logname = flask.session['username']
    connection = insta485.model.get_db()
    operation = flask.request.form['operation']
    username = flask.request.form['username']
    if operation == "follow":
        # Check if user already follows the username
        cur = connection.execute(
            "SELECT * FROM following WHERE username1 = ? AND username2 =?",
            (logname, username)
        )
        existing_follow = cur.fetchone()
        if existing_follow:
            # logname already follows this user
            flask.abort(409)
        else:
            # insert new follow
            connection.execute(
                "INSERT INTO following (username1, username2) VALUES (?, ?)",
                (logname, username)
            )

            # Commit the transaction
            connection.commit()

    elif operation == "unfollow":
        # Check if user already follows username
        cur = connection.execute(
            "SELECT * FROM following WHERE username1 = ? AND username2 = ?",
            (logname, username)
        )
        existing_follow = cur.fetchone()
        if existing_follow:
            print("hello")
            # Remove follower
            connection.execute(
                "DELETE FROM following WHERE username1 = ? AND username2 = ?",
                (logname, username)
            )

            # Commit
            connection.commit()
        else:
            # Logname already doesn't follow username
            flask.abort(409)
    # Redirect back to the target URL
    target_url = flask.request.args.get('target', '/')
    return flask.redirect(target_url)
