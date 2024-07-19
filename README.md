# Instagram Emulator Iteration 1: Server side pages
I have developed this project in VS code.

## Setup
Install Python 3 and Python virtual environment on your local machine.

## Introduction
Insta485 is an Instagram clone that I developed as part of a sequence of projects for EECS 485. The goal of this project is to build an interactive website using server-side dynamic pages with Flask. This project builds on previous work, where I created a static site generator and will be followed by a project involving client-side dynamic pages.

This project demonstrates key concepts such as CRUD (Create, Read, Update, Delete) operations, session management, and SQL database integration. Users can create accounts, log in, follow other users, and interact with posts through likes and comments, similar to how Instagram functions.

## Key Features
- User Authentication: Users can create accounts, log in, and log out.
- User Profiles: Each user has a profile displaying their posts and follower information.
- Follow/Unfollow: Users can follow and unfollow other users.
- Post Creation and Deletion: Users can create and delete posts.
- Commenting: Users can add comments to posts.
- Likes: Users can like and unlike posts.
- Responsive Design: The application is styled to be responsive and user-friendly.

## Running on Local Machine
To get the app up and running, you'll need to start the development server. This server will allow you to see your changes in real-time as you develop the application. Here’s how you can do it:

### Run with Flask Command
First, you'll use the Flask command to start the server. This command will launch the Flask development server in debug mode, which means it will automatically reload if you make any changes to the code and will provide detailed error messages if something goes wrong.

Open your terminal and run the following command:

sh
$ flask --app insta485 --debug run --host 0.0.0.0 --port 8000
Here’s what this command does:

--app insta485: Specifies the Flask application to run.
--debug: Puts the server in debug mode.
--host 0.0.0.0: Makes the server accessible externally by binding it to all available IP addresses.
--port 8000: Runs the server on port 8000.

After running this command, you'll see output indicating that the server is running. You can then open your web browser and navigate to http://localhost:8000/ to see your app in action.

Run Script
To simplify the process of starting your app, you can run the script bin/insta485run that handles all the necessary steps

Using this script makes it easier to start your development server, as you don’t have to remember or type out the full Flask command each time. Simply run the script, and your server will be up and running.

By following these steps, you'll be able to develop and test your app locally, ensuring that all features work correctly before deploying it to a production environment like AWS.

## Database script
This project uses SQLite for managing the database. SQLite is a lightweight SQL database engine stored in a single file on your hard drive. Below are the steps to set up and manage the database for this project.

Installing SQLite
First, ensure you have the SQLite command line utility installed:

For Linux and Windows Subsystem for Linux:
sh
$ sudo apt-get install sqlite3

For macOS:
sh
$ brew install sqlite3

Verify the installation:
$ sqlite3 --version
3.29.0 2019-07-10 17:32:03 fc82b73eaac8b36950e527f12c4b5dc1e147e6f4ad2217ae43ad8288

### Database Management Shell Script
A shell script bin/insta485db is provided to manage the database easily. The script supports the following commands:
create: Initializes the database and populates it with initial data.
destroy: Deletes the database file and any user-generated files.
reset: Resets the database by destroying and then recreating it.
dump: Prints the contents of the database.
By using this script, you can easily manage your SQLite database for development and testing purposes.

## Conclusion
This project demonstrates the implementation of server-side dynamic pages using Flask, handling CRUD operations, sessions, and SQL database usage. I also gained experience with AWS, including cloud-based deployment and managing server instances to deploy this Flask app.
