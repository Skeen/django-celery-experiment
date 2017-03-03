from django.db import models
from django.utils import timezone

class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()

class Task(models.Model):
    id          = models.CharField(max_length=40, primary_key=True)
    created     = models.DateTimeField(default=timezone.now, editable=False)
    modified    = AutoDateTimeField(default=timezone.now)
    state       = models.CharField(max_length=40, null=True)
    #state_meta  = models.CharField(max_length=200, null=True)
    name        = models.CharField(max_length=40, null=True)
    result      = models.CharField(max_length=200, null=True)
    error       = models.CharField(max_length=200, null=True)
    #traceback   = models.CharField(max_length=200, null=True)

    total       = models.IntegerField(default=100);
    current     = models.IntegerField(default=0); 

    def __str__(self):
        return self.id

    def progress(self):
        if(self.state == "STARTED"):
            return self.current / self.total * 100;
        elif(self.state == "SUCCESS"):
            return 100;
        return None

    # We are life, if we've been touched within the last five minutes
    def live(self):
        now = timezone.now()
        return (self.state == "STARTED") and (now - timezone.timedelta(minutes=5) <= self.modified <= now)

    live.boolean = True
