# Generated by Django 3.0.5 on 2021-08-21 21:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20210821_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='reported_on',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
