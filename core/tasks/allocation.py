"""
"""

from celery.task import task

from atmosphere.logger import logger

from core.models.instance import Instance

from datetime import timedelta, datetime

def rtime(instance):
    """
    Run time for the instance.
    """
    return datetime.now() - instance.created_date

def atime(user):
    """
    Allocated time for the time frame.
    """
    t = 0
    return t

@task()
def allocate():
    logger.debug("Allocating Resources...")





