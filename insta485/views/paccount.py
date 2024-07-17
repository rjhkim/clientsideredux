"""Post account requests."""
import os
import uuid
import pathlib
import hashlib
import flask
import insta485


# Used to sign the session cookies
insta485.app.secret_key = os.urandom(24)


def get_target_url():
    """Get the target URL from the query parameters."""
    target_url = flask.request.args.get('target', '/')
    return target_url


def login_user(user_name, password, connection):
    """Log in a user."""
    if not user_name or not password:
        flask.abort(400)
    cur = connection.execute(
        "SELECT users.password "
        "FROM users WHERE username = ?", (user_name,))
    user_act_password = cur.fetchall()
    if not user_act_password:
        flask.abort(403)
    algorithm = 'sha512'
    act_pw_string = user_act_password[0]['password']
    splitter = '$'
    act_pw_salt = act_pw_string.replace(splitter, "*")
    out = act_pw_salt.split("*")
    out = out[1]
    salt = out
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    if user_act_password[0]['password'] != password_db_string:
        flask.abort(403)
    flask.session['username'] = user_name


def create_user(user_name, password, full_name, email, prof_photo):
    """Create a new user account."""
    connection = insta485.model.get_db()
    if not user_name or not password or not full_name \
            or not email or not prof_photo:
        flask.abort(400)
    cur = connection.execute(
        "SELECT users.username "
        "FROM users WHERE username = ?", (user_name,))
    user_found = cur.fetchall()
    if user_found:
        flask.abort(409)
    fileobj = flask.request.files["file"]
    filename = fileobj.filename
    uuid_basename = f"{uuid.uuid4().hex}" \
                    f"{pathlib.Path(filename).suffix.lower()}"
    fileobj.save(insta485.app.config["UPLOAD_FOLDER"] / uuid_basename)
    hash_obj = hashlib.new('sha512')
    hash_obj.update((uuid.uuid4().hex + password).encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join(['sha512', uuid.uuid4().hex, password_hash])
    connection.execute(
        "INSERT INTO users (username, fullname, email, "
        "filename, password) "
        "VALUES (?, ?, ?, ?, ?)",
        (user_name, full_name, email, uuid_basename, password_db_string)
    )
    connection.commit()
    flask.session['username'] = user_name


def delete_user(connection):
    """Delete a user account."""
    if 'username' not in flask.session:
        flask.abort(403)
    else:
        user = flask.session['username']
        connection.execute("DELETE FROM comments WHERE owner=?", (user,))
        connection.execute("DELETE FROM likes WHERE owner=?", (user,))
        cur = connection.execute("SELECT * FROM posts WHERE owner = ? ",
                                 (user,))
        existing_post = cur.fetchall()
        for post in existing_post:
            filename = post['filename']
            file_path = os.path.join(insta485.app.config['UPLOAD_FOLDER'],
                                     filename)
            if os.path.exists(file_path):
                os.remove(file_path)
        connection.execute("DELETE FROM posts WHERE owner=?", (user,))
        connection.execute(
            "DELETE FROM following WHERE "
            "username1=? OR username2=?", (user, user))
        cur2 = connection.execute(
            "SELECT users.filename "
            "FROM users WHERE username = ? ", (user,))
        file = cur2.fetchall()
        filename = file[0]['filename']
        file_path = os.path.join(
            insta485.app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        connection.execute("DELETE FROM users WHERE username=?", (user,))
        connection.commit()
        flask.session.clear()


def edit_user_account(connection):
    """Edit a user's account information."""
    if 'username' not in flask.session:
        flask.abort(403)
    else:
        user = flask.session['username']
        new_name = flask.request.form['fullname']
        new_email = flask.request.form['email']
        new_file = flask.request.files['file']
        if not new_name or not new_file:
            flask.abort(400)
        connection.execute(
            "UPDATE users SET email = ?, fullname = ? "
            "WHERE username = ?", (new_email, new_name, user))
        if new_file:
            cur2 = connection.execute(
                "SELECT users.filename "
                "FROM users WHERE username = ? ", (user,))
            file = cur2.fetchall()
            filename = file[0]['filename']
            file_path = os.path.join(insta485.app.config['UPLOAD_FOLDER'],
                                     filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                fileobj = new_file
                filename = fileobj.filename
            stem = uuid.uuid4().hex
            suffix = pathlib.Path(filename).suffix.lower()
            uuid_basename = f"{stem}{suffix}"
            path = insta485.app.config["UPLOAD_FOLDER"] / uuid_basename
            fileobj.save(path)
            connection.execute(
                "UPDATE users SET filename = ? "
                "WHERE username = ?", (uuid_basename, user))
        connection.commit()


def update_password(connection):
    """Update a user's password."""
    if 'username' not in flask.session:
        flask.abort(403)
    else:
        user = flask.session['username']
        old_pass = flask.request.form['password']
        new_p1 = flask.request.form['new_password1']
        new_p2 = flask.request.form['new_password2']
        if not old_pass or not new_p1 or not new_p2:
            flask.abort(400)
        cur = connection.execute(
            "SELECT users.password FROM users "
            "WHERE username =? ", (user,))
        user_act_password = cur.fetchall()
        act_pw_string = user_act_password[0]['password']
        act_pw_salt = act_pw_string.replace('$', "*")
        out = act_pw_salt.split("*")
        out = out[1]
        salt = out
        hash_obj = hashlib.new('sha512')
        password_salted = salt + old_pass
        hash_obj.update(password_salted.encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        password_db_string = "$".join(['sha512', salt, password_hash])
        if user_act_password[0]['password'] != password_db_string:
            flask.abort(403)
        if new_p1 != new_p2:
            flask.abort(401)
        salt = uuid.uuid4().hex
        hash_obj = hashlib.new('sha512')
        password_salted = salt + new_p1
        hash_obj.update(password_salted.encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        password_db_string = "$".join(['sha512', salt, password_hash])
        connection.execute(
            "UPDATE users SET password = ? "
            "WHERE username = ?", (password_db_string, user))
        connection.commit()


@insta485.app.route('/accounts/', methods=['POST'])
def account_post():
    """Handle account-related POST requests."""
    # Connect to the database
    connection = insta485.model.get_db()
    # Get the operation from the form data
    operation = flask.request.form['operation']
    # Get the target URL
    target_url = get_target_url()
    if operation == 'login':
        user_name = flask.request.form['username']
        password = flask.request.form['password']
        login_user(user_name, password, connection)
        return flask.redirect(target_url)
    if operation == 'create':
        user_name = flask.request.form['username']
        password = flask.request.form['password']
        full_name = flask.request.form['fullname']
        email = flask.request.form['email']
        prof_photo = flask.request.files['file']
        create_user(user_name, password, full_name, email, prof_photo)
        return flask.redirect(target_url)
    if operation == 'delete':
        delete_user(connection)
        return flask.redirect(target_url)
    if operation == 'edit_account':
        edit_user_account(connection)
        return flask.redirect(target_url)
    if operation == 'update_password':
        update_password(connection)
        return flask.redirect(target_url)
    return flask.redirect(target_url)


if __name__ == '__main__':
    insta485.app.run(debug=True)
