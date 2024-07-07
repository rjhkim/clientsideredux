import flask
import insta485
import arrow
from flask import send_from_directory


@insta485.app.route('/posts/<postid>/')
def show_post(postid):

    # Connect to database
    connection = insta485.model.get_db()

    logname = "awdeorio"

    #get all info about post
    cur = connection.execute(
        "SELECT DISTINCT posts.filename AS post_filename, "
        "posts.created AS post_created, "
        "users.filename AS owner_filename, "
        "users.username AS post_owner, "
        "COALESCE(likes_count.likes_count, 0) AS likes_count, "
        "CASE WHEN user_likes.postid IS NOT NULL THEN 1 ELSE 0 END AS user_liked, "
        "comments.commentid, "
        "comments.owner AS comment_owner, "
        "comments.text AS comment_text, "
        "comments.created AS comment_created "
        "FROM posts "
        "JOIN users ON posts.owner = users.username "
        "LEFT JOIN (SELECT DISTINCT postid, COUNT(*) AS likes_count FROM likes GROUP BY postid) likes_count "
        "ON posts.postid = likes_count.postid "
        "LEFT JOIN (SELECT DISTINCT postid FROM likes) user_likes "
        "ON posts.postid = user_likes.postid "
        "LEFT JOIN comments ON posts.postid = comments.postid "
        "LEFT JOIN users AS comment_users ON comments.owner = comment_users.username "
        "WHERE posts.postid = ? "
        "ORDER BY comments.created DESC",
        (postid,)
    )

    results = cur.fetchall()

    print(results)

    post_with_comments = {
        'post_details': {
            'post_filename': results[0]['post_filename'],
            'post_created': arrow.get(results[0]['post_created']).humanize(),
            'post_owner': results[0]['post_owner'],
            'likes_count': results[0]['likes_count'],
            'user_liked': results[0]['user_liked'],
            'owner_filename': results[0]['owner_filename']
        },
        'comments': []
    }

    for row in results:
        if (row['comment_owner'] and row['comment_text'] and row['comment_created']):
            comment_exists = any(
                comment['owner'] == row['comment_owner'] and comment['text'] == row['comment_text']
                and comment['created'] == row['comment_created']
                for comment in post_with_comments['comments']
            )

            if not comment_exists:
                comment = {
                    'owner': row['comment_owner'],
                    'text': row['comment_text'],
                    'created': row['comment_created']
                }
                post_with_comments['comments'].append(comment)


    # Add database info to context
    context = {
        "post_with_comments": post_with_comments,
        "logname": logname
        }
    return flask.render_template("posts.html", **context)