import os
from celery import Celery
from webapp import create_app


def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND'],
        include=['webapp.posts.tasks']
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery


env = os.environ.get("WEBAPP_ENV", "dev")
flask_app = create_app(F"config.{env.capitalize()}Config")

celery = make_celery(flask_app)