# Generated by Django 3.0.5 on 2023-02-11 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_auto_20230211_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]