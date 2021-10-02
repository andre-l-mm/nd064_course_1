import sys
import os
import sqlite3

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
import logging

connection_count = 0
db = 'database.db'


# Check if database is operational.
def check_db():
    if os.path.isfile(db):
        connection = sqlite3.connect(db)
        connection.row_factory = sqlite3.Row
        table = connection.execute(
            'SELECT name FROM sqlite_master WHERE type = "table" AND name = "posts"').fetchone()
        connection.close

        if table is None:
            app.logger.error('Posts table does not exist')
            return False
        else:
            return True
    else:
        app.logger.error('Database file "{}" does not exist!'.format(db))
        return False


# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    global connection_count

    connection = sqlite3.connect(db)
    connection.row_factory = sqlite3.Row

    connection_count += 1

    return connection


# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                              (post_id,)).fetchone()
    connection.close()
    return post


# Count the number of posts in the database
def count_posts():
    connection = get_db_connection()
    count = connection.execute('SELECT count(1) FROM posts').fetchone()
    connection.close()

    return count


# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


# Define the main route of the web application
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)


# Define how each individual article is rendered
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
        app.logger.debug('Article {} does not exist!'.format(post_id))
        return render_template('404.html'), 404
    else:
        app.logger.debug('Article {} retrieved!'.format(post['title']))
        return render_template('post.html', post=post)


# Define the About Us page
@app.route('/about')
def about():
    app.logger.debug('About Us page retrieved!')
    return render_template('about.html')


# Define the post creation functionality
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                               (title, content))
            connection.commit()
            connection.close()
            app.logger.debug('Article titled "{}" created!'.format(title))

            return redirect(url_for('index'))

    return render_template('create.html')


# Define the health monitor endpoint
@app.route("/healthz")
def healthz():
    if check_db():
        response = app.response_class(
            response=json.dumps({"result": "OK - healthy"}),
            status=200,
            mimetype='application/json'
        )
    else:
        response = app.response_class(
            response=json.dumps({"result": "ERROR - unhealthy"}),
            status=500,
            mimetype='application/json'
        )

    return response


# Define the metrics endpoint
@app.route("/metrics")
def metrics():
    response = app.response_class(
        response=json.dumps({
            "db_connection_count": connection_count,
            "post_count": count_posts()[0],
        }),
        status=200,
        mimetype='application/json'
    )

    return response


# Configure default logging to log to both stdout and stderror as requested.
# This will duplicate all log lines on the terminal but it is what is being asked in the assignement.
# The format used is the same as logging.BASIC_FORMAT with the addition of a timestamp between brackets.
def configure_log():
    format = '%(levelname)s:%(name)s:[%(asctime)s]:%(message)s'
    level = logging.DEBUG
    handlers = [get_handler(sys.stdout, format, level),
                get_handler(sys.stderr, format, level)]
    logging.basicConfig(level=level, handlers=handlers)


# Creates a new stream logging handler with the provided stream, format and logging level.
def get_handler(stream, format, level):
    handler = logging.StreamHandler(stream)
    handler.setLevel(level)
    formatter = logging.Formatter(format)
    handler.setFormatter(formatter)

    return handler


# configure log outputing to both stdout and stderr as requested - This generates duplicated logs on terminal
configure_log()

# start the application on port 3111
if __name__ == "__main__":
    app.run(host='0.0.0.0', port='3111')
