from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Comments, Profile, Sprint, Issue, Project, MyTodo


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
    created_by = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(SprintSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Sprint
        fields = '__all__'
        extra_kwargs = {"display_id": {"required": False, "allow_null": True}}

    def create(self, validated_data):
        return Sprint.objects.create(**validated_data)


class IssuesSerializer(serializers.ModelSerializer):
    project_abbr = serializers.SerializerMethodField('get_project_abbr')

    def get_project_abbr(self, Issue):
        return Issue.project.abbr

    class Meta:
        model = Issue
        fields = '__all__'
        extra_fields = ['project_abbr']


class ProjectsSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Project
        fields = '__all__'


class MyTodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyTodo
        fields = '__all__'


class CommentsSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    user_info = UserSerializer(source="created_by", read_only=True)

    class Meta:
        model = Comments
        fields = '__all__'
        extra_fields = ['user_info']
