from django.contrib import admin

from .models import Task

class TaskAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    readonly_fields=('created','succeeded','running',)
    
    list_display = ('id', 'created', 'modified', 'state')

    ordering = ('-created',)

admin.site.register(Task, TaskAdmin);
