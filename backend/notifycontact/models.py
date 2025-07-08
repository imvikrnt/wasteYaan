from django.db import models

class Contacts(models.Model):
    name = models.CharField(max_length=100)               
    email = models.EmailField(max_length=100)                
    mobile = models.CharField(max_length=15)                 
    message = models.TextField()                            
    created_at = models.DateTimeField(auto_now_add=True)     

    def __str__(self):
        return f"{self.name} - {self.email}"

class Advertisement(models.Model):
    advt_no = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
    file = models.FileField(upload_to='advertisements/')

    def __str__(self):
        return f"{self.advt_no} - {self.title}"
    

class Notification(models.Model):
    to_mail = models.EmailField()
    from_mail = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.to_mail}"