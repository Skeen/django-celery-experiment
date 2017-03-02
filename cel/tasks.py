# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


import time
import random

@shared_task(bind=True)
def do_work(self, total):
    """ Calculate something important async, update state """
    for i in range(total):
        print(i)
        self.update_state(state='PROGRESS',
            meta={'current': i, 'total': total})
        time.sleep(1);

    if random.random() < 0.5:
        return "do_work done"
    else:
        raise ValueError("do_work failed")

