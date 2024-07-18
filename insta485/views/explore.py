import flask
import insta485
import arrow
from flask import send_from_directory


@insta485.app.route('/explore/')
def get_explore():
    # This page lists all users that the logged in user
    # is not following and includes icon, username
    # with link to /users/user
    # also follow button
    if 'username' not in flask.session:
        return flask.redirect("/accounts/login/")
    logname = flask.session['username']
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT users.username AS user, users.filename AS filename "
        "FROM users "
        "LEFT JOIN following ON users.username = following.username2 "
        "WHERE users.username NOT IN ( "
        "    SELECT following.username2 "
        "    FROM following "
        "    WHERE following.username1 = ? "
        ") "
        "AND users.username != ?",
        (logname, logname,)
    )
    results = cur.fetchall()
    res = {}
    for row in results:
        user = row['user']
        res[user] = {
            'filename': row['filename'],
        }
    context = {"res": res,
               "logname": logname}
    return flask.render_template("explore.html", **context)
