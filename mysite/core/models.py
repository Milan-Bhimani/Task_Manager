from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth.models import User
# 1. New Team Model
class Team(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)  # Optional description

    def __str__(self):
        return self.name

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length= 100)
    age = models.IntegerField(
        validators = [
            MinValueValidator(0),
            MaxValueValidator(120)
        ]
    )
    user = models.ForeignKey(User, on_delete= models.SET_NULL, null = True, blank= True)

    # ForeignKey: Link to Team
    # related_name='members' allows us to do team.members.all()
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
    # ManyToMany: A Person can have many Skills
    skills = models.ManyToManyField('Skills', blank=True)

    def __str__(self):
        return self.name

class Skills(models.Model):
    name = models.CharField(max_length= 100)

    def __str__(self):
        return self.name
class Profile(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)

    bio = models.TextField(blank = True)
    github_url = models.URLField(blank = True)

    def __str__(self):
        return f"Profile of {self.person.name}"
    