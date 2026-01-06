from rest_framework import serializers
from .models import Task,Project

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def validate_project(self, value):
        user = self.context['request'].user
        if value.owner != user:
            raise serializers.ValidationError("You cannot add tasks to a project you do not own.")
        return value

class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['owner']
            