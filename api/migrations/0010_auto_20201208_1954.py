# Generated by Django 3.1.3 on 2020-12-08 14:24

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0009_sprint_project'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MyTodos',
            new_name='MyTodo',
        ),
    ]
