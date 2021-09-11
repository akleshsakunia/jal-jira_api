from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.decorators import action, api_view
from .models import Sprint, Issue, Project, MyTodo
from .serializers import UserSerializer, SprintSerializer, IssuesSerializer, ProjectsSerializer, MyTodoSerializer
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


class MyTodoViewSet(viewsets.ModelViewSet):
    queryset = MyTodo.objects.all()
    serializer_class = MyTodoSerializer
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

    def get(self, request, format=None):
        """
        Return sprint board items.
        """
        print('pk is:', request.user.pk)
        user = User.objects.get(pk=request.user.pk)
        default_project = user.profile.default_project or user.profile.tagged_projects.all()[
            0]
        project = Project.objects.get(pk=default_project.pk)
        sprint_issues = Issue.objects.filter(sprint_id=project.curr_sprint)
        serialized_data = IssuesSerializer(sprint_issues, many=True).data
        return Response(serialized_data)
