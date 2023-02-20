from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.decorators import action, api_view
from .models import Comments, Sprint, Issue, Project, MyTodo
from .serializers import CommentsSerializer, UserSerializer, SprintSerializer, IssuesSerializer, ProjectsSerializer, MyTodoSerializer
from django.db.models import Q


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, )


class SprintViewSet(viewsets.ModelViewSet):
    queryset = Sprint.objects.all()
    serializer_class = SprintSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(created_by=user)
        serializer.save(updated_by=user)

    def perform_update(self, serializer):
        user = self.request.user
        serializer.save(updated_by=user)


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssuesSerializer
    permission_classes = (permissions.IsAuthenticated, )


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectsSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(created_by=user)
        created_project = serializer.save(updated_by=user)
        user.profile.tagged_projects.add(created_project)

    def perform_update(self, serializer):
        user = self.request.user
        serializer.save(updated_by=user)


class MyTodoViewSet(viewsets.ModelViewSet):
    queryset = MyTodo.objects.all()
    serializer_class = MyTodoSerializer
    permission_classes = (permissions.IsAuthenticated, )


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = (permissions.IsAuthenticated, )


class ListIssuesAssignedToUser(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, pk, format=None):
        """
        Return a list of all users.
        """
        assigned_issues = Issue.objects.filter(assignee=pk)
        serialized_data = IssuesSerializer(assigned_issues, many=True).data
        return Response(serialized_data)


class ListUsersIssues(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, pk, format=None):
        """
        Return a list of all users.
        """
        users_issues = Issue.objects.filter(Q(assignee=pk) | Q(reporter=pk))
        serialized_data = IssuesSerializer(users_issues, many=True).data
        return Response(serialized_data)


class ListUsersProjects(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, format=None):
        """
        Return a list of all users projects.
        """
        print('pk is:', request.user.pk)
        user = User.objects.get(pk=request.user.pk)
        tagged_projects = user.profile.tagged_projects
        serialized_data = ProjectsSerializer(tagged_projects, many=True).data
        return Response(serialized_data)


class ListSprintIssues(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, project_key=None, format=None):
        """
        Return sprint board items.
        """
        if not project_key:
            user = User.objects.get(pk=request.user.pk)
            default_project = user.profile.default_project or user.profile.tagged_projects.all()[
                0]
        project = Project.objects.get(pk=project_key or default_project.pk)
        sprint_issues = Issue.objects.filter(sprint_id=project.curr_sprint)
        serialized_data = IssuesSerializer(sprint_issues, many=True).data
        return Response(serialized_data)


class ListIssueComments(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, pk, format=None):
        """
        Return a list of all issue comments.
        """
        comments = Comments.objects.filter(issue_id=pk)
        serialized_data = CommentsSerializer(
            comments,
            context={'request': request},
            many=True).data
        return Response(serialized_data)


class ListProjectUsers(APIView):
    """Returns list of users tagged to a project"""
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, project_key, format=None):
        """
        Return a list of all issue comments.
        """
        users = User.objects.filter(profile__tagged_projects=project_key)
        serialized_data = UserSerializer(
            users,
            many=True).data
        return Response(serialized_data)


class ListProjectSprints(APIView):
    """Returns list of active sprints tagged to a project"""
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, project_key, format=None):
        project_active_sprint = Sprint.objects.filter(
            project=project_key, status=Sprint.SprintStatus.ACTIVE.value)
        serialized_data = SprintSerializer(
            project_active_sprint,
            many=True).data
        return Response(serialized_data)
