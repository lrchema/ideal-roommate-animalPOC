from flask import Flask
import mysql.connector

def create_app():
    app = Flask(__name__)

    # blueprint for auth routes in our app
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

# app = create_app()

def dbconn():
    hostname = 'localhost'
    username = 'root'
    password = 'password'
    database = 'testdb'
    return mysql.connector.connect(host=hostname, user=username, passwd=password, db=database)