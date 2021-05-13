from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from .models import Sprint, Issue, Project, MyTodo
from .serializers import UserSerializer, SprintSerializer, IssuesSerializer, ProjectsSerializer, MyTodoSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, )


class SprintViewSet(viewsets.ModelViewSet):
    queryset = Sprint.objects.all()
    serializer_class = SprintSerializer
    permission_classes = (permissions.IsAuthenticated, )


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

class ListUsersIssues(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, pk, format=None):
        """
        Return a list of all users.
        """
        assigned_issues = Issue.objects.filter(assignee=pk)
        serialized_data = IssuesSerializer(assigned_issues, many=True).data
        return Response(serialized_data)