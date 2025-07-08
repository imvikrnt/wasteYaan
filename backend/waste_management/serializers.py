from rest_framework import serializers
from waste_management.models import Complaint
from api.models import User  # Importing User model

class ComplaintSerializer(serializers.ModelSerializer):
    # Accepting user_id from the frontend
    user_id = serializers.CharField(write_only=True)

    class Meta:
        model = Complaint
        fields = [
            'user_id', 'waste_type', 'description', 
            'address', 'area', 'status', 'date', 'waste_image'
        ]

    def validate_user_id(self, value):
        # print("userfor valid user value",value)
        """
        Validate whether the user_id exists and has the role 'user'.
        """
        try:
            user = User.objects.get(id=value)
            # print("userfor valid user id",user)
            if user.role != "user":
                raise serializers.ValidationError("Only users can create complaints.")
        except User.DoesNotExist:
            raise serializers.ValidationError("User ID not found.")
        return value

    def create(self, validated_data):
        # Get the user object using user_id
        user = User.objects.get(id=validated_data.pop('user_id'))
        # Create the complaint object with the associated user
        return Complaint.objects.create(user=user, **validated_data)




class WasteComplaintListSerializer(serializers.ModelSerializer):
    # Overriding the user_id field to return user data from api.model if it exists
    user_name = serializers.SerializerMethodField()
    assigned_to_name = serializers.SerializerMethodField()

    class Meta:
        model = Complaint
        fields = ['id','waste_type', 'area', 'description', 'status', 'date','waste_image','user_id', 'assigned_to_id','user_name', 'assigned_to_name', ]

    def get_user_name(self, obj):
        """Return user name from api.model's user_id"""
        user = None
        if obj.user_id:  # If user_id exists
            try:
                user = User.objects.get(id=obj.user_id)  # Fetch user data from api.model
            except User.DoesNotExist:
                user = None
        return user.user_id if user else None  # Return user name or None if not found

    def get_assigned_to_name(self, obj):
        """Return assigned_to name from api.model's assigned_to_id"""
        assigned_user = None
        if obj.assigned_to_id:  # If assigned_to_id exists
            try:
                assigned_user = User.objects.get(id=obj.assigned_to_id)  # Fetch assigned user data
            except User.DoesNotExist:
                assigned_user = None
        return assigned_user.user_id if assigned_user else None  # Return
    # user_name = serializers.SerializerMethodField()
    # assigned_to_name = serializers.SerializerMethodField()

    # class Meta:
    #     model = Complaint
    #     # Directly define fields as a tuple
    #     fields = ('id', 'area', 'description', 'status', 'created_at', 'updated_at', 
    #               'user_id', 'assigned_to_id', 'users_id', 'assigned_to_name')

    # def get_users_id(self, obj):
    #     try:
    #         # Fetch the user object using the user_id
    #         user = User.objects.get(id=obj.user_id)
    #         return user.user_id  # Return the user's name
    #     except User.DoesNotExist:
    #         return "Unknown User"  # Return a default message if user not found

    # def get_assigned_to_user_id(self, obj):
    #     try:
    #         # Check if assigned_to_id is not null
    #         if obj.assigned_to_id is None:
    #             return None  # Return null if assigned_to_id is not set
            
    #         # Fetch the assigned user object using the assigned_to_id
    #         assigned_user = User.objects.get(id=obj.assigned_to_id)
    #         return assigned_user.user_id # Return the assigned user's name
        
    #     except User.DoesNotExist:
    #         return "Unknown User"  # Return a default message if the assigned user is not found
    # # class Meta:
    #     model = Complaint
    #     fields = '__all__'

