# Generated by Django 3.1.3 on 2020-12-08 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20201208_1825'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='abbr',
            field=models.CharField(default='zui', max_length=5, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='project_title',
            field=models.CharField(default='proj ttl', max_length=50, unique=True),
            preserve_default=False,
        ),
    ]
