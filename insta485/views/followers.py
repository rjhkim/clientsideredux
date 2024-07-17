import flask
import insta485
import arrow
from flask import send_from_directory

@insta485.app.route('/users/<username>/followers/')
def get_followers(username):
    #get the filename, username of each users
    #check if logname follows this person

    logname = "awdeorio"

    connection = insta485.model.get_db()

    # Check if the user exists
    cur_user_check = connection.execute(
        "SELECT 1 FROM users WHERE username = ?",
        (username,)
    )
    user_exists = cur_user_check.fetchone()

    if not user_exists:
        abort(404)

    cur1 = connection.execute(
        "SELECT u.filename, f.username1, f.username2 FROM users u "
        "LEFT JOIN following f ON u.username = f.username1 "
        "WHERE f.username2 = ?",
        (username, )
    )
    followers = cur1.fetchall()
    print(followers)
    cur2 = connection.execute(
        "SELECT f.username2 "
        "FROM following f LEFT JOIN users u ON  f.username1 = u.username "
        "WHERE f.username1 = ?",
        (username, )
    )
    check = cur2.fetchall()

    context = {
        "followers": followers,
        "check": check,
        "logname": logname
    }
    return flask.render_template("followers.html", **context)

