from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


class Project(models.Model):
    class ProjectStatus(models.TextChoices):
        ACTIVE = 'ACT'
        INACTIVE = 'INACT'
    # fields
    project_title = models.CharField(max_length=50, blank=False, unique=True)
    abbr = models.CharField(max_length=5, blank=False, unique=True)
    short_description = models.CharField(max_length=50, blank=False)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=10, choices=ProjectStatus.choices, default=ProjectStatus.ACTIVE)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, editable=False, related_name='%(class)s_created_by')
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, editable=False, related_name='%(class)s_updated_by')

    @property
    def project_id(self):
        return self.id

    def __str__(self):
        return str(self.project_title)

class Profile(models.Model):
    # constants
    # USER_STATUS = models.TextChoices('ACTIVE', 'INACTIVE', 'COMPROMISED')
    # one-to-one link to django's user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # fields
    # status = models.CharField(max_length=15, blank=False, choices=USER_STATUS)
    bio = models.CharField(max_length=50, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    tagged_projects = models.ForeignKey(
        Project, null=True, blank=True, on_delete=models.CASCADE, related_name='projects')

    class meta:
        ordering = ['id']


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Sprint(models.Model):
    # no id let it be handled by django internally using its own id field
    class SprintStatus(models.TextChoices):
        ACTIVE = 'ACT'
        INACTIVE = 'INACT'
    class Meta:
        unique_together = (('display_id', 'project'),)

    # fields
    display_id = models.IntegerField() # will be incremented per project
    short_description = models.CharField(max_length=50, blank=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=10, choices=SprintStatus.choices, default=SprintStatus.INACTIVE)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='project')
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, editable=False, related_name='%(class)s_created_by')
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, editable=False, related_name='%(class)s_updated_by')

    @property
    def sprint_id(self):
        return self.id

    def __str__(self):
        return str(self.sprint_id)
    
    def save(self, *args, **kwargs):
        if self._state.adding:
            last_id = self.__class__.objects.filter(project_id=self.project_id).order_by('-id')
            self.display_id = last_id[0].display_id + 1 if last_id else 1

        super(Sprint, self).save(*args, **kwargs)



class Issue(models.Model):
    class IssueStatus(models.TextChoices):
        INPROGRESS = 'IN_PROG'
        DONE = 'DONE'
        TESTING = 'TESTING'
        TESTED = 'TESTED'
        BLOCKED = 'BLOCKED'
        TODO = 'TODO'

    class IssueType(models.TextChoices):
        TASK = 'TASK'
        STORY = 'STORY'
        BUG = 'BUG'

    class PRIORITY(models.TextChoices):
        HIGH = 'HIGH'
        MEDIUM = 'MEDIUM'
        LOW = 'LOW'

    # fields
    assignee = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name='assignee')
    reporter = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='reporter')
    issue_title = models.CharField(max_length=25, blank=False)
    description = models.CharField(max_length=100, blank=True)
    reported_on = models.DateField(auto_now_add=True)
    start_date = models.DateField(null=True, blank=True)
    resolution_date = models.DateField(null=True, blank=True)
    estimate = models.CharField(max_length=50, blank=True)
    sprint = models.ForeignKey(
        Sprint, null=True, blank=True, on_delete=models.CASCADE)
    issue_status = models.CharField(
        max_length=15, choices=IssueStatus.choices, default=IssueStatus.TODO)
    issue_type = models.CharField(
        max_length=15, choices=IssueType.choices, default=IssueType.TASK)
    relates_to = models.ManyToManyField('self', blank=True)
    priority = models.CharField(
        max_length=15, choices=PRIORITY.choices, default=PRIORITY.LOW)

    def __str__(self):
        return str(self.issue_title)


class MyTodo(models.Model):
    class TodoStatus(models.TextChoices):
        OPEN = 'OPEN'
        CLOSED = 'CLOSED'
    # fields
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_id')
    description = models.CharField(max_length=100)
    status = models.CharField(
        max_length=10, choices=TodoStatus.choices, default=TodoStatus.OPEN)
    created_on = models.DateField(auto_now_add=True)
