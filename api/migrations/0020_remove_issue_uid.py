# Generated by Django 3.0.5 on 2023-02-20 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_auto_20230220_1615'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issue',
            name='uid',
        ),
    ]
