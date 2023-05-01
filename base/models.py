from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.core.validators import URLValidator
from django.conf import settings


TYPE_CHOICES = [
    ('image', 'Image'),
    ('file', 'File'),
    ('link', 'Link'),
]


class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    username = None
    hackathons = models.ManyToManyField(
        'Hackathon', blank=True, related_name='participants')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def enrolled_hackathons(self):
        return Hackathon.objects.filter(participants=self)


class Hackathon(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    background_image = models.ImageField(upload_to='hackathons/')
    hackathon_image = models.ImageField(upload_to='hackathons/')

    submission_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    reward_prize = models.CharField(max_length=255)


class Submissions(models.Model):
    SUBMISSION_TYPES = (
        ('image', 'Image'),
        ('file', 'File'),
        ('link', 'Link')
    )

    name = models.CharField(max_length=255)
    summary = models.TextField()
    submission_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    submission_file = models.FileField(
        upload_to='submissions/', blank=True, null=True)
    submission_image = models.ImageField(
        upload_to='submissions/', blank=True, null=True)
    submission_link = models.URLField(blank=True, null=True)
    hackathon = models.ForeignKey(
        Hackathon, on_delete=models.CASCADE, related_name='submissions')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submissions')

    def __str__(self):
        return self.name
