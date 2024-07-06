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

    #this query selects each followers username and filename who follows the user
    #query checks if logname follows this username
    cur = connection.execute(
        "SELECT DISTINCT users.filename as filename, users.username as user, "
        "CASE WHEN follow_exists.username1 IS NOT NULL THEN 1 ELSE 0 END as follow_existing "
        "FROM users "
        "LEFT JOIN following ON users.username = following.username1 "
        "LEFT JOIN (SELECT username1 from following WHERE username1 = ?) follow_exists "
        "WHERE following.username2 = ? ",
        (logname, username,)
    )

    results = cur.fetchall()

    print(results)
    res = {}
    for row in results:
        user = row['user']

        res[user] = {
            'filename': row['filename'],
            'follow_existing': row['follow_existing']
        }

    context = {"res": res,
               "logname": logname}
    return flask.render_template("followers.html", **context)

