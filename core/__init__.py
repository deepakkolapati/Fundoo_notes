from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail

db = SQLAlchemy()
migarte = Migrate()
mail = Mail()

def init_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:9033@localhost:5432/fundoo_notes'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'deepakchandu9@gmail.com'
    app.config['MAIL_PASSWORD'] = 'nkng rovm okmq qidd'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    mail.init_app(app)
    db.init_app(app)
    migarte.init_app(app, db)

    return app