from django.contrib import admin

# Register your models here.
from .models import Project, Task

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "start_date")
    search_fields = ("name", "owner__username")
    list_filter = ("start_date",)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "priority", "status", "due_date")
    search_fields = ("title", "project__name")
    list_filter = ("priority", "status", "due_date")

