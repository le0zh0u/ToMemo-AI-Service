from flask_sqlalchemy import SQLAlchemy

mysql = SQLAlchemy()

def connect_to_mysql(app):
    mysql.init_app(app)