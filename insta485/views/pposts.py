"""Handle post request for posts."""
import pathlib
import uuid
import os
import flask
import insta485


@insta485.app.route('/posts/', methods=['POST'])
def post_post():
    """Handle post request for posts."""
    if 'username' not in flask.session:
        return flask.redirect("/accounts/login/")
    logname = flask.session['username']
    connection = insta485.model.get_db()
    operation = flask.request.form['operation']
    if operation == 'create':
        # Unpack flask object
        fileobj = flask.request.files["file"]
        filename = fileobj.filename
        # Check if the file is empty
        if not filename:
            flask.abort(400)
        else:
            # Compute base name (filename without directory).
            # We use a UUID to avoid
            # clashes with existing files, and
            # ensure that the name is compatible with the
            # filesystem.
            # For best practive, we ensure uniform file extensions
            # (e.g.lowercase).
            stem = uuid.uuid4().hex
            suffix = pathlib.Path(filename).suffix.lower()
            uuid_basename = f"{stem}{suffix}"

            # Save to disk
            path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
            fileobj.save(path)

            connection.execute(
                "INSERT INTO posts (owner, filename) VALUES (?, ?)",
                (logname, uuid_basename)
            )

            connection.commit()
    elif operation == 'delete':
        postid = flask.request.form['postid']

        # Check if the user owns the post and abort(403) if not
        # Perform database operations to check ownership and delete
        cur = connection.execute(
            "SELECT * FROM posts WHERE owner = ? AND postid = ?",
            (logname, postid)
        )
        cur2 = connection.execute(
            "SELECT * FROM users WHERE username = ?",
            (logname,)
        )
        # user owns the post:
        if cur.fetchone() and cur2.fetchone():
            # Get the filename associated with the post
            cur = connection.execute(
                "SELECT filename FROM posts WHERE postid = ?",
                (postid,)
            )
            filename_row = cur.fetchone()
            # Check if a filename was found
            if filename_row is not None:
                filename = filename_row['filename']
                # Construct the full path to the file
                file_path = os.path.join(insta485.app.config['UPLOAD_FOLDER'],
                                         filename)
                # Check if the file exists and delete it
                if os.path.exists(file_path):
                    os.remove(file_path)
            # Remove everything in the database related to this post
            connection.execute(
                "DELETE FROM posts WHERE postid = ?",
                (postid,)
            )
            # Commit the transaction (important!)
            connection.commit()

    # Redirect back to the target URL
    target_url = flask.request.args.get('target', f'/users/{logname}/')
    return flask.redirect(target_url)
