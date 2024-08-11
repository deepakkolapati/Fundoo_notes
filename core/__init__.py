from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from settings import settings

db = SQLAlchemy()
migarte = Migrate()
mail = Mail()

class Development:
    SQLALCHEMY_DATABASE_URI = settings.database_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True

class Testing:
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.sqlite3"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    TESTING= True

class Production:
    SQLALCHEMY_DATABASE_URI = settings.database_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = False

config_mode={
    "debug": Development,
    "testing": Testing,
    "production": Production
}

def init_app(mode="debug"):
    app = Flask(__name__)
    app.config.from_object(config_mode[mode])
    app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://127.0.0.1:6379/0",
        result_backend="redis://127.0.0.1:6379/0",
        broker_connection_retry_on_startup=True,
        # task_ignore_result=True,
        redbeat_redis_url = "redis://localhost:6379/0",
        redbeat_lock_key = None,
        enable_utc=True,
        beat_max_loop_interval=5,
        beat_scheduler='redbeat.schedulers.RedBeatScheduler'
    ),
)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = settings.mail_port
    app.config['MAIL_USERNAME'] = settings.sender
    app.config['MAIL_PASSWORD'] = settings.mail_password
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    mail.init_app(app)
    db.init_app(app)
    migarte.init_app(app, db)
    with app.app_context():
        db.create_all()
    return app