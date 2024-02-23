from celery import Celery, Task,shared_task
from . import init_app as fapp
from flask_mail import Message
from . import mail
from settings import settings

def celery_init_app(app) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.conf.enable_utc = False
    celery_app.conf.timezone = 'Asia/Kolkata'
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

app=fapp()
celery=celery_init_app(app)

@shared_task
def celery_send_mail(user, email, token):
    msg=Message("Welcome to Fundoo_Notes! Verify Your Email to Get Started",
                sender=f"{settings.sender}",recipients=[email])
    
    with open('message.txt') as file:
        content = file.read()
        content = content.format(user=user, base_url=settings.base_url, token=token, sender=settings.sender)
        msg.body= content
    mail.send(msg)