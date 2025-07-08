from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models import User  
from django.shortcuts import get_object_or_404
from api.serializers import SafeUserSerializer
from waste_management.serializers import ComplaintSerializer
from waste_management.models import Complaint

class AdminProfileDataView(APIView):
    def get(self, request):
        user_id = request.query_params.get('id')
        
        if not user_id:
            return Response({"error": "Missing ID"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = get_object_or_404(User, id=user_id)
        except:
            return Response({"error": "Invalid User ID"}, status=status.HTTP_400_BAD_REQUEST)

        admin_profile_data = {
            "id":user.id,
            "role": user.role,
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email,
            "mobile":user.mobile,
            "dob":user.dob,
            "gender":user.gender,
            "nationality":user.nationality,
            "profile_img": user.profile_img.url if user.profile_img and hasattr(user.profile_img, 'url') else None,
            # "profile_img":user.profile_img,
        }
        print("fatech data ",admin_profile_data)
        return Response(admin_profile_data, status=status.HTTP_200_OK)
        
class AdminDashboardDataView(APIView):
    def get(self, request):
        user_id = request.query_params.get('id')
        
        if not user_id:
            return Response({"error": "Missing ID"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = get_object_or_404(User, id=user_id)
        except:
            return Response({"error": "Invalid User ID"}, status=status.HTTP_400_BAD_REQUEST)

        total_users = User.objects.filter(role="User").count()
        total_supervisors = User.objects.filter(role="Supervisor").count()
        total_collectors = User.objects.filter(role="Collector").count()
        total_complaint = Complaint.objects.count()

        admin_data = {
            "id":user.id,
            "name": user.name,
            "email": user.email,
            "user_id": user.user_id,
            "role": user.role,
            "total_users": total_users,
            "total_supervisors": total_supervisors,
            "total_collectors": total_collectors,
            'total_complaints':total_complaint,
        }
        # print(admin_data)
        return Response(admin_data, status=status.HTTP_200_OK)

class UserRoleListView(APIView):
    def get(self, request):
        # Get the 'role' query parameter, default is None (no filtering)
        role = request.query_params.get('role', None)
        print(role)
        if role:
            # If role is provided, filter by role
            users = User.objects.filter(role=role)
        else:
            # If no role is provided, get all users
            users = User.objects.all()
        
        # Serialize the user data
        serializer = SafeUserSerializer(users, many=True)
        # print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

class WasteComplaintListView(APIView):
    def get(self, request):
        complaints = Complaint.objects.all()

        if not complaints.exists():
            return Response(
                {"message": "No complaints found."},
                status=status.HTTP_200_OK
            )

        serializer = ComplaintSerializer(complaints, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserUpdateActivityStatusView(APIView):
    """
    Update the activity status of a user based on userId and boolean value.
    """

    def post(self, request):
        print(request.data)
        try:
            user_id = request.data.get('userId')
            is_active = request.data.get('is_active')

            # Check if the required fields are present
            if user_id is None or is_active is None:
                return Response(
                    {'error': 'userId and is_active are required fields.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Convert to boolean in case the value is a string
            if isinstance(is_active, str):
                is_active = is_active.lower() == 'true'

            # Find the user by ID
            try:
                user = User.objects.get(id=user_id)
                # Update the is_active status
                user.is_active = is_active
                user.save()

                return Response(
                    {'message': f'User status updated to {"Active" if is_active else "Inactive"} successfully!'},
                    status=status.HTTP_200_OK
                )
            except User.DoesNotExist:
                return Response(
                    {'error': 'User not found.'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        except Exception as e:
            return Response(
                {'error': f'An error occurred: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# ========================================================================================================
# AREA & ASSIGN VIEWS
from .models import Area,CollectorAssign
from .serializers import UserListSerializer, AreaListSerializer, CollectorAssignSerializer


class AddAreaView(APIView):
    def post(self, request):
        area_name = request.data.get('area_name')

        # Check if the area name already exists
        if Area.objects.filter(area_name=area_name).exists():
            return Response(
                {"error": "Area with this name already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create the new area
        new_area = Area(area_name=area_name)
        new_area.save()

        # Prepare the response data
        response_data = {
            "message": "Area added successfully",
            "area_name": new_area.area_name
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

class SupervisorAreaListView(APIView):
    def get(self, request):
        # Get list of supervisors
        supervisors = User.objects.filter(role='supervisor')
        supervisor_serializer = UserListSerializer(supervisors, many=True)

         # Get list of collectors
        collectors = User.objects.filter(role='collector')
        collectors_serializer = UserListSerializer(collectors, many=True)

        # Get list of areas
        areas = Area.objects.all()
        area_serializer = AreaListSerializer(areas, many=True)
        # print("supervior :",supervisor_serializer.data, 'area :',area_serializer.data)
        return Response({
            'supervisors': supervisor_serializer.data,
            'collectors': collectors_serializer.data,
            'areas': area_serializer.data
        }, status=status.HTTP_200_OK)   

class UpdateAsignAreaSupervisorView(APIView):
    def post(self, request):
        try:
            # Get the area ID and supervisor ID from the request data
            area_id = request.data.get("id")
            supervisor_id = request.data.get("supervisorassigned_id")

            # Validate the required data
            if not area_id or not supervisor_id:
                return Response({"error": "Both area ID and supervisor ID are required."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Fetch the area by the given ID
            try:
                area = Area.objects.get(id=area_id)
            except Area.DoesNotExist:
                return Response({"error": "Area not found"}, status=status.HTTP_404_NOT_FOUND)

            # Validate if the supervisor exists
            try:
                supervisor = User.objects.get(id=supervisor_id)
            except User.DoesNotExist:
                return Response({"error": "Supervisor not found"}, status=status.HTTP_404_NOT_FOUND)

            # Update the supervisor assignment
            area.supervisorassigned_id = supervisor_id
            area.is_assigned = True
            area.save()

            return Response({"message": "Supervisor assigned successfully!"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CollectorAssignView(APIView):
    def post(self, request):
        try:
            # Get the collector ID and supervisor ID from the request data
            collector_id = request.data.get("collector_id")
            supervisor_id = request.data.get("supervisor_id")
            print(f"Received Collector ID: {collector_id}, Supervisor ID: {supervisor_id}")

            # Validate the required data
            if not collector_id or not supervisor_id:
                return Response(
                    {"error": "Both collector ID and supervisor ID are required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Validate if the collector exists
            try:
                collector = User.objects.get(id=collector_id)
                print(f"Collector found: {collector}")
            except User.DoesNotExist:
                print("Collector not found")
                return Response({"error": "Collector not found"}, status=status.HTTP_404_NOT_FOUND)

            # Validate if the supervisor exists
            try:
                supervisor = User.objects.get(id=supervisor_id)
                print(f"Supervisor found: {supervisor}")
            except User.DoesNotExist:
                print("Supervisor not found")
                return Response({"error": "Supervisor not found"}, status=status.HTTP_404_NOT_FOUND)

            # Check if the collector is already assigned to any supervisor
            existing_assignment = CollectorAssign.objects.filter(collectorassigned=collector).first()
            if existing_assignment:
                print("Collector already assigned to a supervisor.")
                return Response(
                    {"error": f"Collector already assigned to supervisor ID: {existing_assignment.supervisorassigned_id}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create or update the CollectorAssign instance
            try:
                collector_assign, created = CollectorAssign.objects.update_or_create(
                    collectorassigned=collector,  # Correctly reference the User instance
                    defaults={
                        'supervisorassigned': supervisor,  # Correctly reference the User instance
                        'is_assigned': True
                    }
                )
                print(f"Collector assignment successful: {collector_assign}")
            except Exception as e:
                print(f"Error during assignment: {str(e)}")
                return Response({"error": "Error during assignment."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Return success message
            message = "Collector assigned successfully!" if created else "Collector assignment updated successfully!"
            return Response({"message": message}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)