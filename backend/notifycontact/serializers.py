from rest_framework import serializers
from .models import Contacts,Advertisement,Notification

class NotifyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = ['id', 'name', 'email', 'mobile', 'message', 'created_at']


class NotificationContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ['advt_no', 'title', 'description', 'date', 'file']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

