from django.db import models
from django.contrib.auth.models import User



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    name = models.CharField(max_length=100, blank=True, null=True)
    surname = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    total_points = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Law(models.Model):
    title = models.CharField(max_length=200)
    image = models.URLField(blank=True, null=True)  # For image URLs from Cloudinary
    video = models.URLField(blank=True, null=True) 
    sub = models.TextField()
    description = models.TextField()
    story = models.TextField()
    points = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)  # Automatically set the field to now when the object is first created
    updated = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.title
    
class LegalCase(models.Model):
    OPTION_CHOICES = [
        ('1', 'Option 1'),
        ('2', 'Option 2'),
    ]
    
    law = models.ForeignKey(Law, on_delete=models.CASCADE)
    scenario = models.TextField()
    option_1 = models.CharField(max_length=255)
    option_2 = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1, choices=OPTION_CHOICES)

    def __str__(self):
        return f"LegalCase {self.id}: {self.scenario[:50]}..."
    
class Quiz(models.Model):
    OPTION_CHOICES = [
        ('A', 'Option 1'),
        ('B', 'Option 2'),
        ('C', 'Option 3'),
        ('D', 'Option 4'),
    ]

    law = models.ForeignKey(Law, on_delete=models.CASCADE)
    question = models.TextField()
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=1, choices=OPTION_CHOICES)
    points = models.PositiveIntegerField(default=1) 

    def __str__(self):
        return self.question



