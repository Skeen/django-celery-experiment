from django.contrib import admin

from .models import Task

import numbers

class TaskAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def progress(self, obj):
        percent = obj.progress();
        if(isinstance(percent, numbers.Number)):
            return "{0:.2f} %".format(obj.progress());
        else:
            return percent;

    readonly_fields=('id', 'created', 'modified', 'state', 'progress', 'result', 'error', 'live', 'total', 'current')
    
    list_display = ('id', 'name', 'modified', 'state', 'progress', 'live')

    ordering = ('-modified',)

admin.site.register(Task, TaskAdmin);
