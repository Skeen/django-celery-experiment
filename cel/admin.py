from django.contrib import admin

from .models import Task

import numbers
from django.utils.html import format_html

class TaskAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def progress(self, obj):
        percent = obj.progress();
        if(isinstance(percent, numbers.Number)):
            return "{0:.2f} %".format(obj.progress());
        else:
            return percent;

    def resulta(self, obj):
        print("WOW");
        #return '%s' % obj.result;
        return format_html('<br/><pre>%s</pre>' % obj.result);

    readonly_fields=('id', 'created', 'modified', 'state', 'progress', 'result', 'resulta', 'error', 'live', 'total', 'current')
    
    list_display = ('id', 'name', 'modified', 'state', 'progress', 'live')

    ordering = ('-modified',)

admin.site.register(Task, TaskAdmin);
