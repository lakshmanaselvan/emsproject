from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    ROLE_CHOICE = (
        ('Student', 'Student'),
        ('HOD_CSE', 'HOD_CSE'),
        ('HOD_MECH', 'HOD_MECH'),
        ('HOD_CIVIL', 'HOD_CIVIL'),
        ('HOD_EEE', 'HOD_EEE'),
        ('HOD_ECE', 'HOD_ECE'),
        ('Principal','Principal'),
        ('Event_Manager','Event_Manager'),
        ('Assistant Professor', 'Assistant Professor')
    )
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True, null = True)
    password = models.CharField(max_length=200, null = True)
    is_verified = models.BooleanField(default = False)
    token = models.CharField(max_length=100, default=None)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    role = models.CharField(max_length = 200, choices = ROLE_CHOICE)
    has_module_perms = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class Venue(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Categorie(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField('Title',max_length=200)
    description  = models.TextField('Description')
    organizer = models.ForeignKey(UserProfile, on_delete = models.CASCADE, null=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete = models.CASCADE)
    startTime = models.TimeField(blank=False, null=True)
    endTime = models.TimeField(blank=False, null=True)
    startDate = models.DateField(blank=False, null=True)
    endDate = models.DateField(blank=False, null=True)
    chief_guest = models.CharField(max_length = 200, null = True)
    approval = models.BooleanField(default = False)
    def __str__(self):
        return self.title
