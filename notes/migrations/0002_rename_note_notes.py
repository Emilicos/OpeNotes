# Generated by Django 4.2.7 on 2023-11-28 10:52

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_remove_course_year'),
        ('course', '0003_course_prerequisites'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Note',
            new_name='Notes',
        ),
    ]
