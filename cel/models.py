from django.db import models
from django.utils import timezone

from celery.result import AsyncResult
import json

class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()

class Task(models.Model):
    id          = models.CharField(max_length=40, primary_key=True)
    created     = models.DateTimeField(default=timezone.now, editable=False)
    modified    = AutoDateTimeField(default=timezone.now)

    def __str__(self):
        return self.id

    def progress(self):
        job = AsyncResult(self.id)
        if(job.state == 'PROGRESS'):
            return json.dumps(job.result)
        else:
            return "{}";

    def state(self):
        job = AsyncResult(self.id)
        return job.state


    def failure(self):
        job = AsyncResult(self.id)
        if(job.state == 'FAILURE'):
            return job.traceback
        else:
            return "";


    def result(self):
        job = AsyncResult(self.id)
        if(job.state == 'SUCCESS'):
            return job.result
        else:
            return "";

    def succeeded(self):
        job = AsyncResult(self.id)
        return job.successful();

    def running(self):
        job = AsyncResult(self.id)
        return job.ready();

    succeeded.boolean = True
    succeeded.short_description = 'Successful'
    running.boolean = True
