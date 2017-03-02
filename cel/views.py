from django.shortcuts import render

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .tasks import add, do_work
from .models import Task

class IndexView(generic.ListView):
    template_name = 'cel/index.html'
    context_object_name = 'task_list'

    def get_queryset(self):
        """
        Return the last five published tasks
        """
        return Task.objects.all().order_by('-created')[:5]


class DetailView(generic.DetailView):
    model = Task
    template_name = 'cel/detail.html'

def test(request):
    job = add.delay(4,4);
    value = job.get(timeout=10);
    return HttpResponse("Hello 4 + 4 = " + str(value))


def start(request):
    """ Start a computationally intensive job, then forward to the waiting page """
    job = do_work.delay(total=60)
    task = Task(id = job.id)
    task.save()
    return HttpResponseRedirect(reverse('cel:detail', kwargs={'pk': task.id}))


def progress(request, task_id):
    """ Poll the status of the task and report it to the user """
    
    task = Task.objects.get(id=task_id)
    return HttpResponse(task.progress(), content_type='application/json')


def state(request, task_id):
    """ Check if the task has failed """
    task = Task.objects.get(id=task_id)
    return HttpResponse(task.state())


def failure(request, task_id):
    """ Check if the task has failed """
    task = Task.objects.get(id=task_id)
    return HttpResponse(task.failure())


def result(request, task_id):
    """ Check if the task has failed """
    task = Task.objects.get(id=task_id)
    return HttpResponse(task.result())
