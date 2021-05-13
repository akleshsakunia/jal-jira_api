from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Sprint, Issue, Project, MyTodo


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name', 'email', 'is_staff', 'profile')


class SprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = '__all__'

    def create(self, validated_data):
        return Sprint.objects.create(**validated_data)


class IssuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'


class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class MyTodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyTodo
        fields = '__all__'
