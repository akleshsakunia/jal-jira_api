from django.contrib import admin
from .models import Comments, Profile, Sprint, Issue, Project, MyTodo


@admin.register(Profile)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    # list_filter = ('type',)


@admin.register(Sprint)
class SprintAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_description', 'start_date', 'status')
    exclude = ('display_id', )


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('reporter', 'issue_title', 'sprint')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'project_title', 'start_date', 'status')


@admin.register(MyTodo)
class MytodoAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'status')


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('comment', 'created_by', 'issue_id')
