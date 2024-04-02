# Generated by Django 5.0.3 on 2024-03-20 19:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AttendEaseApp', '0004_customuser_mentor'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Course',
            new_name='Department',
        ),
        migrations.RenameField(
            model_name='department',
            old_name='course_code',
            new_name='dept_id',
        ),
        migrations.RenameField(
            model_name='department',
            old_name='course_name',
            new_name='dept_name',
        ),
        migrations.RenameField(
            model_name='subject',
            old_name='course',
            new_name='department',
        ),
        migrations.AddField(
            model_name='mcsubmission',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='slsubmission',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]