from django.contrib import admin

# Register your models here.
from .models import Person, Team, Skills, Profile

@admin.register(Person)

class PersonAdmin(admin.ModelAdmin):
    list_display = ("name","age")
    search_fields = ("name",)
    list_filter = ("age",)
    

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)
    list_filter = ("name",)


@admin.register(Skills)
class SkillsAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_filter = ("name",)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("bio", "github_url")
    search_fields = ("bio",)
    list_filter = ("bio",)