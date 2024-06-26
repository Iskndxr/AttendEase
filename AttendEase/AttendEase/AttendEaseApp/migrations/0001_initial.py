# Generated by Django 5.0.3 on 2024-03-19 18:40

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClassSession',
            fields=[
                ('session_code', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_code', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('course_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MCsubmission',
            fields=[
                ('mc_id', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('submission_date', models.DateField()),
                ('mc_proof', models.FileField(upload_to='media/MCproofs')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('remarks', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('P', 'Pending'), ('A', 'Approved'), ('R', 'Rejected'), ('S', 'Suspicious')], default='P', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='SLsubmission',
            fields=[
                ('sl_id', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('submission_date', models.DateField()),
                ('sl_proof', models.FileField(upload_to='media/SLproofs')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('justification', models.TextField()),
                ('remarks', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('P', 'Pending'), ('A', 'Approved'), ('R', 'Rejected')], default='P', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('identifier', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('is_lecturer', models.BooleanField(default=False)),
                ('is_uttk', models.BooleanField(default=False)),
                ('is_tphea', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('first_name', models.CharField(blank=True, max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('profile_completed', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('subject_code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('subject_name', models.CharField(max_length=100)),
                ('credit_hours', models.IntegerField(validators=[django.core.validators.MaxValueValidator(6)])),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AttendEaseApp.course')),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('class_name', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AttendEaseApp.subject')),
                ('lecturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('P', 'Present'), ('A', 'Absent'), ('MC', 'Sick Leave'), ('SL', 'Special Leave')], max_length=2)),
                ('class_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AttendEaseApp.classsession')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
