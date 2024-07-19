"""
Insta485 index (main) view.

URLs include:
/
"""
import os
import flask
import arrow
from flask import send_from_directory
import insta485


@insta485.app.route('/')
def show_index():
    """Display / route."""
    if 'username' not in flask.session:
        return flask.redirect("/accounts/login/")
    logname = flask.session['username']
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
    cur = connection.execute(
        "SELECT posts.postid, "
        "posts.filename AS post_filename, "
        "posts.created AS post_created, "
        "users.username AS post_owner, "
        "users.filename AS owner_filename, "
        "users.fullname AS owner_fullname, "
        "COALESCE(likes_count.likes_count, 0) AS likes_count, "
        "CASE WHEN user_likes.postid IS NOT NULL "
        "THEN 1 ELSE 0 END AS user_liked, "
        "comments.commentid, "
        "comments.owner AS comment_owner, "
        "comments.text AS comment_text, "
        "comments.created AS comment_created "
        "FROM posts "
        "JOIN users ON posts.owner = users.username "
        "LEFT JOIN (SELECT postid, COUNT(*) AS likes_count "
        "FROM likes GROUP BY postid) likes_count "
        "ON posts.postid = likes_count.postid "
        "LEFT JOIN (SELECT postid FROM likes WHERE owner = ?) user_likes "
        "ON posts.postid = user_likes.postid "
        "LEFT JOIN comments ON posts.postid = comments.postid "
        "LEFT JOIN users AS comment_users "
        "ON comments.owner = comment_users.username "
        "WHERE posts.owner = ? "
        "OR posts.owner IN (SELECT username2 "
        "FROM following WHERE username1 = ?) "
        "ORDER BY posts.created DESC, "
        "posts.postid DESC, comments.created DESC",
        (logname, logname, logname)
    )
    results = cur.fetchall()
    posts_with_comments = {}
    for row in results:
        post_id = row['postid']
        if post_id not in posts_with_comments:
            posts_with_comments[post_id] = {
                'post_details': {
                    'postid': row['postid'],
                    'post_filename': row['post_filename'],
                    'post_created': arrow.get(row['post_created']).humanize(),
                    'post_owner': row['post_owner'],
                    'owner_filename': row['owner_filename'],
                    'likes': row['likes_count'],
                    'user_liked': row['user_liked']
                },
                'comments': []
             }
        # adding comments now
        if (row['comment_owner'] and row['comment_text']
                and row['comment_created']):
            comment_exists = any(
                comment['owner'] == row['comment_owner']
                and comment['text'] == row['comment_text']
                and comment['created'] == row['comment_created']
                for comment in posts_with_comments[post_id]['comments']
            )
            if not comment_exists:
                comment = {
                    'owner': row['comment_owner'],
                    'text': row['comment_text'],
                    'created': row['comment_created']
                }
                posts_with_comments[post_id]['comments'].append(comment)
    # Add database info to context
    context = {"posts_with_comments": posts_with_comments}
    return flask.render_template("index.html", **context)


@insta485.app.route("/uploads/<path:filename>")
def send_image(filename):
    """Send images."""
    if 'username' not in flask.session:
        flask.abort(403)
    file_path = os.path.join(insta485.app.config['UPLOAD_FOLDER'], filename)
    # Check if the file exists and delete it
    if not os.path.exists(file_path):
        flask.abort(404)
    return send_from_directory(insta485.app.config['UPLOAD_FOLDER'], filename)
