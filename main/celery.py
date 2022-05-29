import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

app = Celery('main')

# Setup to use all the variables in settings
# that begins with 'CELERY_'
app.config_from_object('django.conf:settings', namespace='CELERY')

# Setting up Celery to “autodiscover” tasks from all apps
# app.autodiscover_tasks()

# Dummy task for debbug
# A task being bound means the first argument
# to the task will always be the task instance
# (self)
# https://docs.celeryq.dev/en/stable/userguide/tasks.html
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std-setting-beat_schedule
# The periodic task schedule used by beat.
# app.conf.beat_schedule = {
#     'every-4-minutes_kenobi': {
#         'task': 'base.tasks.kenobi',
#         'schedule': crontab(minute='*/4')  # execute every 4 minutes
#     },
#     'every-1-minutes_add': {
#         'task': 'base.tasks.add',
#         'schedule': crontab(minute='*/1'), # every 1 minute
#         'args': (16, 16),
#     },
#     'every-4-minutes_grievous': {
#         'task': 'base.tasks.grievous',
#         'schedule': crontab(minute='*/4') # execute every 4 minutes
#     },
# }
