import flask
import insta485
import arrow
from flask import send_from_directory

@insta485.app.route('/users/<username>/followers/')
def get_user(username):
    #get the filename, username of each users
    #check if logname follows this person

    logname = "awdeorio"

    connection = insta485.model.get_db()

    cur1 = connection.execute