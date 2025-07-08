from rest_framework import serializers
from .models import Area,CollectorAssign
from api.models import User 

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id', 'area_name', 'supervisorassigned', 'collectorassigned', 'is_assigned']

        
class CollectorAssignSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectorAssign
        fields = ['id',  'supervisorassigned', 'collectorassigned', 'is_assigned']

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'user_id', 'role']

class AreaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id', 'area_name','is_assigned']