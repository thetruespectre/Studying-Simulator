from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pfp = models.ImageField(default="def_pfp.svg")
    bio = models.TextField(null=True, blank=True)
    name = models.CharField(default=AbstractUser.USERNAME_FIELD, null=True, blank=True, max_length=200)
    email = models.EmailField(unique=True) 
    username = models.CharField(max_length=200, unique=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    
    def __str__(self):
        return self.email

class Subject(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Classroom(models.Model):
    name = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    is_updated = models.BooleanField(default=False)
    
    participants = models.ManyToManyField(User, related_name="participants", blank=True)
    
    class Meta:
        ordering = ["-updated", "-created"]
    
    def __str__(self):
        return self.name
    
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    body = models.TextField()
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    is_updated = models.BooleanField(default=False)
    
    class Meta:
        ordering = ["-updated", "-created"]
    
    def __str__(self):
        return self.body[:50]
    