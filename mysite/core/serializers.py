from rest_framework import serializers
from .models import Person, Team, Skills, Profile

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team 
        fields = ['id', 'name', 'description']

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = ['id','name']

class PerofileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile 
        fields = ['bio', 'github_url']

class PersonSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    profile = PerofileSerializer(read_only=True)
    class Meta:
        model = Person
        fields = ['id', 'name', 'age', 'team', 'skills', 'profile']