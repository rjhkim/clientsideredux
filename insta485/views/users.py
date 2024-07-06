import flask
import insta485
import arrow
from flask import send_from_directory

@insta485.app.route('/users/<username>/')
def get_user(username):
    connection = insta485.model.get_db()

    logname = "awdeorio"

    #name of username - 
    #follower count - 
    #following count - 
    #following bool - 
    #post count - 
    #images for all posts - 

    # Check if the user exists
    cur_user_check = connection.execute(
        "SELECT 1 FROM users WHERE username = ?",
        (username,)
    )
    user_exists = cur_user_check.fetchone()

    if not user_exists:
        abort(404)


    #post count and the username
    cur1 = connection.execute(
        "SELECT posts.owner as owner, COUNT(*) as post_count, posts.filename as file, users.fullname as fullname "
        "FROM posts "
        "LEFT JOIN users ON posts.owner = users.username "
        "WHERE posts.owner = ? ",
        (username,)
    )

    post_details = cur1.fetchall()


    #following bool
    cur2 = connection.execute(
        "SELECT following.username1 "
        "FROM following "
        "WHERE username1 = ? AND username2 = ?",
        (logname, username)
    )

    follow_bool = cur2.fetchall()

    #follower count
    cur3 = connection.execute(
        "SELECT DISTINCT COUNT(*) as count "
        "FROM following "
        "WHERE username2 = ? ",
        (username,)
    )

    follower_count = cur3.fetchall()

    print(follower_count)

    #following count
    cur4 = connection.execute(
        "SELECT DISTINCT COUNT(*) as count "
        "FROM following "
        "WHERE username1 = ? ",
        (username,)
    )

    following_count = cur4.fetchall()

    #get all pictures

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