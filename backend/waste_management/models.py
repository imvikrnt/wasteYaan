# models.py (in waste_management app)

from django.db import models
from api.models import User  


class Complaint(models.Model):
    WASTE_TYPES = [
        ("Plastic", "Plastic"),
        ("Organic", "Organic"),
        ("E-waste", "E-waste"),
        ("Other", "Other"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Only registered users can create complaints
    waste_type = models.CharField(max_length=50, choices=WASTE_TYPES)
    description = models.TextField()
    address = models.CharField(max_length=255)
    area = models.CharField(max_length=100)
    waste_image = models.ImageField(upload_to="complaints/")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    date = models.DateTimeField(auto_now_add=True)  # Automatically set the date when the complaint is created
    assigned_to = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name='assigned_complaints'
    )  # A supervisor/collector can be assigned later

    def __str__(self):
        return f"Complaint by {self.user.username} - {self.waste_type}"
