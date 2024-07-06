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
        "SELECT COUNT(*) as count "
        "FROM following "
        "WHERE username2 = ? ",
        (logname,)
    )

    follower_count = cur3.fetchall()

    #following count
    cur4 = connection.execute(
        "SELECT COUNT(*) as count "
        "FROM following "
        "WHERE username1 = ? ",
        (logname,)
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

    print(filename)

    context = {
        "post_details": post_details,
        "follow_bool": follow_bool,
        "follower_count": follower_count,
        "following_count": following_count,
        "logname": logname,
        "filename": filename
    }

    return flask.render_template("users.html", **context)