from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'role', 'name', 'dob', 'gender', 'nationality', 'mobile', 'email', 'password', 'profile_img', 'otp']

# serializers.py
class SafeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'role', 'name', 'dob', 'gender', 'nationality', 'mobile', 'email', 'profile_img', 'user_id', 'is_active']




# from rest_framework import serializers
# from .models import User
# from django.contrib.auth.hashers import make_password

# class RegisterSerializer(serializers.ModelSerializer):
#     confirm_email = serializers.EmailField(write_only=True)
#     confirm_password = serializers.CharField(write_only=True)
#     captcha = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = [
#             'role', 'name', 'dob', 'gender', 'nationality',
#             'mobile', 'email', 'confirm_email',
#             'password', 'confirm_password',
#             'captcha',
#         ]
#         extra_kwargs = {
#             'password': {'write_only': True},
#         }

#     def validate(self, data):
#         if data['email'] != data['confirm_email']:
#             raise serializers.ValidationError("Emails do not match.")
#         if data['password'] != data['confirm_password']:
#             raise serializers.ValidationError("Passwords do not match.")

#         # Add simple captcha validation
#         if data['captcha'] != "4r2T8":
#             raise serializers.ValidationError("Invalid captcha.")

#         return data

#     def create(self, validated_data):
#         validated_data.pop('confirm_email')
#         validated_data.pop('confirm_password')
#         validated_data.pop('captcha')
#         validated_data['password'] = make_password(validated_data['password'])
#         return super().create(validated_data)
