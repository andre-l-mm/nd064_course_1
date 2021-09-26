# TechTreds Web Application

This is a Flask application that lists the latest articles within the cloud-native ecosystem.

## Run 

To run this application there are 2 steps required:

1. Initialize the database by using the `python init_db.py` command. This will create or overwrite the `database.db` file that is used by the web application.
2.  Run the TechTrends application by using the `python app.py` command. The application is running on port `3111` and you can access it by querying the `http://127.0.0.1:3111/` endpoint.


## Commands Used
```
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment (always run this when openning a new terminal)
cd .venv
source bin/activate

# Initialize the database
python init_db.py

# Upgrade pip
pip install --upgrade pip

# Install required packages
pip install -r requirements.txt

# Start the application
python app.py

# Go to http://127.0.0.1:3111/

# Using flask command line to start the application
# This can be used to automatically apply source code changes but runs on port 5000 instead of 3111
FLASK_APP=app.py FLASK_ENV=development flask run

# Go to http://127.0.0.1:5000/
```

