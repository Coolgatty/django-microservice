from .celery import app as celery_app

# This code ensures that Celery finds the
# tasks you’ve written when your Django
# application starts.
__all__ = ['celery_app']
