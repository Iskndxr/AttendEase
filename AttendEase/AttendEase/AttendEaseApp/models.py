from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MaxValueValidator
from django.db import models, transaction
from django.db.utils import IntegrityError
import random, string


class Department(models.Model):
    dept_id = models.CharField(primary_key=True, max_length=5)
    dept_name = models.CharField(max_length=100)

class Subject(models.Model):
    subject_code = models.CharField(primary_key=True, max_length=10)
    subject_name = models.CharField(max_length=100)
    credit_hours = models.IntegerField(validators=[MaxValueValidator(6)])
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

class CustomUserManager(BaseUserManager):
    def create_user(self, identifier, password=None, **extra_fields):
        if not identifier:
            raise ValueError('The identifier field must be set')
        user = self.model(identifier=identifier, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, identifier, password, **extra_fields):
        extra_fields.setdefault('is_admin', True) 
        return self.create_user(identifier, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    identifier = models.CharField(primary_key=True, max_length=20, unique=True)
    is_student = models.BooleanField(default=False)
    is_lecturer = models.BooleanField(default=False)
    is_uttk = models.BooleanField(default=False)
    is_tphea = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    mentor = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    profile_completed = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'identifier'

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

class Class(models.Model):
    class_name = models.CharField(primary_key=True, max_length=6)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    lecturer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class ClassSession(models.Model):
    session_code = models.CharField(primary_key=True, max_length=20)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def generate_session_code(self, length=8):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    
    def save(self, *args, **kwargs):
        if not self.session_code:
            self.session_code = self.generate_session_code()
            while ClassSession.objects.filter(session_code=self.session_code).exists():
                self.session_code = self.generate_session_code()
        super().save(*args, **kwargs)

class Attendance(models.Model):
    ATTENDANCEstatus_choices = (
        ('P', 'Present'),
        ('A', 'Absent'),
        ('MC', 'Sick Leave'),
        ('SL', 'Special Leave'),
    )
    class_session = models.ForeignKey(ClassSession, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=ATTENDANCEstatus_choices)

class MCsubmission(models.Model):
    MCstatus_choices = (
        ('P', 'Pending'),
        ('A', 'Approved'),
        ('R', 'Rejected'),
        ('S', 'Suspicious'),
    )
    mc_id = models.CharField(primary_key=True, unique=True, max_length=10)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    submission_date = models.DateField()
    mc_proof = models.FileField(upload_to='media/MCproofs')
    start_date = models.DateField()
    end_date = models.DateField()
    remarks = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=2, choices=MCstatus_choices, default='P')


    def save(self, *args, **kwargs):
        with transaction.atomic():
            if not self.mc_id:
                prefix = 'MC'
                try:
                    latest = MCsubmission.objects.latest('mc_id')
                    next_id = int(latest.mc_id.replace(prefix, '')) + 1
                except MCsubmission.DoesNotExist:
                    next_id = 1  

                self.mc_id = f"{prefix}{next_id}"
                while MCsubmission.objects.filter(mc_id=self.mc_id).exists():
                    next_id += 1
                    self.mc_id = f"{prefix}{next_id}"

            super().save(*args, **kwargs)

class SLsubmission(models.Model):
    SLstatus_choices = (
        ('P', 'Pending'),
        ('A', 'Approved'),
        ('R', 'Rejected'),
    )
    sl_id = models.CharField(primary_key=True, unique=True, max_length=10)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    submission_date = models.DateField()
    sl_proof = models.FileField(upload_to='media/SLproofs')
    start_date = models.DateField()
    end_date = models.DateField()
    justification = models.TextField()
    remarks = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=2, choices=SLstatus_choices, default='P')

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if not self.sl_id:
                prefix = 'SL'
                try:
                    latest = SLsubmission.objects.latest('sl_id')
                    next_id = int(latest.sl_id.replace(prefix, '')) + 1
                except SLsubmission.DoesNotExist:
                    next_id = 1 

                self.sl_id = f"{prefix}{next_id}"
                while SLsubmission.objects.filter(sl_id=self.sl_id).exists():
                    next_id += 1
                    self.sl_id = f"{prefix}{next_id}"

            super().save(*args, **kwargs)