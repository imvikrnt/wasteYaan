from django.db import models
import random
import string

class User(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('supervisor', 'Supervisor'),
        ('collector', 'Collector'),
        ('user', 'User'),
    ]
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    NATIONALITY_CHOICES = [
        ('indian', 'Indian'),
        ('others', 'Others'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    name = models.CharField(max_length=255)
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    nationality = models.CharField(max_length=100, choices=NATIONALITY_CHOICES, default='Indian')
    mobile = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Store hashed password
    profile_img = models.ImageField(upload_to='profile_pics/', default='profile_pics/default_profile.png')
    otp = models.CharField(max_length=10, null=True, blank=True)
    user_id = models.CharField(max_length=12, unique=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.user_id})"

    def generate_unique_id(self):
        if self.role == 'admin':
            prefix = 'AD'
        elif self.role == 'supervisor':
            prefix = 'SUP'
        elif self.role == 'collector':
            prefix = 'COL'
        else:
            prefix = 'NDU'  # Normal Default User

        random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        return prefix + random_string

    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = self.generate_unique_id()
        super(User, self).save(*args, **kwargs)

