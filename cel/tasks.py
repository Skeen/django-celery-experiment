# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

# TODO: Do database handler using this:
#http://docs.celeryproject.org/en/latest/userguide/tasks.html#task-inheritance

import celery
from celery.result import AsyncResult
from .models import Task

import json

class DumpTask(celery.Task):

    def delay(self, *args, **kwargs):
        res = super(DumpTask, self).delay(*args, **kwargs);
        task = Task(id = res.id)
        task.name = self.name
        task.save()
        return res;

    #def run(self, *args, **kwargs):
    #    task = Task(id = self.request.id)
    #    task.name = self.name
    #    task.save()
    #    return super(DumpTask, self).run(*args, **kwargs);

    def update_state(self, task_id=None, state=None, meta=None):
        task = Task.objects.get(id=self.request.id)
        task.state = state;
        #task.state_meta = json.dumps(meta);
        task.save();
        return super(DumpTask, self).update_state(task_id, state, meta);

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        task = Task.objects.get(id=self.request.id)
        task.state = "FAILURE";
        task.error = str(exc)
        # TODO: Hack traceback support in again
        #task.traceback = exc.format_exc();
        task.save();
        return super(DumpTask, self).on_failure(exc, task_id, args, kwargs, einfo);

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        task = Task.objects.get(id=self.request.id)
        task.state = "RETRY";
        task.save();
        return super(DumpTask, self).on_retry(exc, task_id, args, kwargs, einfo);

    def on_success(self, retval, task_id, args, kwargs):
        task = Task.objects.get(id=self.request.id)
        task.state = "SUCCESS";
        task.result = retval;
        task.save();
        return super(DumpTask, self).on_success(retval, task_id, args, kwargs);

    # Set the total number of subtasks to do
    def setTotal(self, value):
        task, created = Task.objects.get_or_create(id=self.request.id)
        task.name = self.name
        task.total = value;
        task.save();

    # We just did one subtask
    def incrementCurrent(self):
        task = Task.objects.get(id=self.request.id)
        task.current += 1;
        if(task.current > task.total):
            raise ValueError("Incrementing current above total!");
        task.save();

    # We did 'x' subtasks at this point
    def setCurrent(self, value):
        task = Task.objects.get(id=self.request.id)
        task.current = value;
        if(task.current > task.total):
            raise ValueError("Setting current above total!");
        task.save();

from celery.task.schedules import crontab
from celery.decorators import periodic_task
import requests
import re

from django.utils import encoding

def escape_ansi(line):
    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)

@shared_task(base=DumpTask, bind=True, name="periodic_task")
def some_task(self):
    self.setTotal(1);
    r = requests.get("http://wttr.in/Aarhus");
    self.incrementCurrent();
    utf8string = r.content.decode("utf8")
    utf8short = '\n'.join(utf8string.split('\n')[:7]);
    print(utf8short);
    return escape_ansi(utf8short)
    #return utf8short #encoding.smart_str(utf8short, encoding='ascii', errors='replace')

@shared_task(base=DumpTask, bind=True)
def add(self, x, y):
    self.setTotal(1);
    value = x + y;
    self.incrementCurrent();
    return value

import time
import random

@shared_task(base=DumpTask, bind=True)
def do_work(self, total, failure):
    """ Calculate something important async, update state """
    self.setTotal(total);
    self.update_state(state="STARTED");
    for i in range(total):
        #print(i)
        self.incrementCurrent();
        time.sleep(1);

    if failure:
        raise ValueError("do_work failed")
    else:
        return "do_work done"
