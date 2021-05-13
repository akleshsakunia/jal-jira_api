from django.urls import include, path
from rest_framework import routers
from . import views
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, 'users')
router.register(r'sprints', views.SprintViewSet, 'sprints')
router.register(r'issues', views.IssueViewSet, 'issues')
router.register(r'projects', views.ProjectViewSet, 'projects')
router.register(r'mytodos', views.MyTodoViewSet, 'mytodos')

urlpatterns = [
    path('', include(router.urls)),
    path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(r'api-token-auth/', obtain_jwt_token),
    path(r'api-token-refresh/', refresh_jwt_token),
    path(r'auth-jwt-verify/', verify_jwt_token),
    path(r'assigned-issues/user/<int:pk>/', views.ListUsersIssues.as_view(), name='assigned_issues')
]
