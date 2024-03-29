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
    created_by_user = UserSerializer(source="created_by", read_only=True)
    updated_by_user = UserSerializer(source="updated_by", read_only=True)

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(SprintSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Sprint
        fields = '__all__'
        extra_fields = ['created_by_user', 'updated_by_user']
        extra_kwargs = {"display_id": {"required": False, "allow_null": True}}

    def create(self, validated_data):
        return Sprint.objects.create(**validated_data)


class IssuesSerializer(serializers.ModelSerializer):
    project_abbr = serializers.SerializerMethodField('get_project_abbr')
    uid = serializers.SerializerMethodField('get_uid')

    def get_project_abbr(self, Issue):
        return Issue.project.abbr

    def get_uid(self, Issue):
        return "-".join([Issue.project.abbr, str(Issue.id)])

    class Meta:
        model = Issue
        fields = '__all__'
        extra_fields = ['project_abbr', 'uid']


class ProjectsSerializer(serializers.ModelSerializer):
    created_by_user = UserSerializer(source="created_by", read_only=True)
    updated_by_user = UserSerializer(source="updated_by", read_only=True)

    class Meta:
        model = Project
        fields = '__all__'
        extra_fields = ['created_by_user', 'updated_by_user']


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
