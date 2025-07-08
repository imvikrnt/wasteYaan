from django.db import models
from api.models import User 

class Area(models.Model):
    # Area name (unique)
    area_name = models.CharField(max_length=100, unique=True)
    
    # Supervisor assigned by Admin (Optional initially)
    supervisorassigned = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_supervisor'
    )
    
    # Collector assigned by Supervisor (Optional initially)
    collectorassigned = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_collector'
    )
    
    # Assignment status (Default: False)
    is_assigned = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.area_name} - Assigned: {self.is_assigned}"


class CollectorAssign(models.Model):
       
    # Supervisor assigned by Admin (Optional initially)
    supervisorassigned = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigne_supervisors'
    )
    
    # Collector assigned by Supervisor (Optional initially)
    collectorassigned = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigne_collectors'
    )
    
    # Assignment status (Default: False)
    is_assigned = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.supervisorassigned} - Assigned: {self.is_assigned}"

