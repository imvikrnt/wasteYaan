from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from waste_management.serializers import ComplaintSerializer,WasteComplaintListSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Complaint
from django.shortcuts import get_object_or_404

# from .serializers import ComplaintSerializer
from .models import User  # Your custom User model
from notifycontact.models import Notification  # Assuming this is your model
from notifycontact.utils import send_notification_email  # Your custom email sender

class CreateComplaintView(APIView):
    def post(self, request):
        print(request.data)
        try:
            # Step 1: Save complaint
            serializer = ComplaintSerializer(data=request.data)
            if serializer.is_valid():
                complaint = serializer.save()

                # Step 2: Get user from user ID in request
                user_id = request.data.get('user_id')
                user = get_object_or_404(User, id=user_id)

                # Step 3: Send mail
                subject = "Complaint Registered"
                message = f"""
                Hello {user.name},

                Your complaint (ID: {complaint.id}) has been successfully registered.
                Thank you for reporting.

                Regards,
                Wasteyaan Team
                """
                send_notification_email(
                    from_mail="esmshelpline@gmail.com",
                    to_mail=user.email,
                    subject=subject,
                    message=message
                )

                # Step 4: Store in Notification model
                Notification.objects.create(
                    to_mail=user.email,
                    from_mail="esmshelpline@gmail.com",
                    subject=subject,
                    message=message
                )

                return Response(
                    {"message": "Complaint created and notification sent."},
                    status=status.HTTP_201_CREATED
                )
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print("Exception:", str(e))
            return Response({"message": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class CreateComplaintView(APIView):
#     def post(self, request):
#         try:
#             serializer = ComplaintSerializer(data=request.data)

#             # Validate and save the data
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(
#                     {"message": "Complaint created successfully."},
#                     status=status.HTTP_201_CREATED
#                 )

#             # Print errors if validation fails
#             print("Serializer errors:", serializer.errors)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         except Exception as e:
#             print("Exception:", str(e))
#             return Response({"message": "An internal error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ComplaintListView(APIView):
    def get(self, request):
        try:
            # Fetch all complaints from the database
            complaints = Complaint.objects.all()
            
            # Serialize the data
            serializer =WasteComplaintListSerializer(complaints, many=True)
            
            # Return the serialized data as JSON response
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AssignCollectorView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this view

    def post(self, request, complaint_id):
        # Ensure the user is a supervisor
        if not request.user.groups.filter(name='Supervisor').exists():
            return Response({"detail": "You don't have permission to assign collectors."}, status=status.HTTP_403_FORBIDDEN)

        # Find the complaint
        try:
            complaint = Complaint.objects.get(id=complaint_id)
        except Complaint.DoesNotExist:
            return Response({"detail": "Complaint not found."}, status=status.HTTP_404_NOT_FOUND)

        # Assign collector
        collector = request.data.get('collector')
        complaint.assigned_to = collector
        complaint.save()

        return Response({"message": "Collector assigned successfully."}, status=status.HTTP_200_OK)

# class UpdatePickupStatusView(APIView):
#     def put(self, request, pickup_id):
#         new_status = request.data.get('status')

#         if not new_status:
#             return Response({'error': 'Status field is required'}, status=status.HTTP_400_BAD_REQUEST)

#         # Replace Complaint with your actual model (e.g., Pickup)
#         pickup = get_object_or_404(Complaint, id=pickup_id)
#         pickup.status = new_status
#         pickup.save()

#         return Response({'message': 'Status updated successfully'}, status=status.HTTP_200_OK)


class UpdatePickupStatusView(APIView):
    def put(self, request,pickup_id):
        try:
            # pickup_id = request.data.get('pickup_id')
            new_status = request.data.get('status')

            if not pickup_id or not new_status:
                return Response({"error": "pickup_id and status are required"}, status=400)

            # Step 1: Get the complaint
            complaint = get_object_or_404(Complaint, id=pickup_id)
            complaint.status = new_status
            complaint.save()

            # Step 2: Get the user
            user = get_object_or_404(User, id=complaint.user_id)

            # Step 3: Prepare email content
            subject = f"Your Complaint #{complaint.id} has been {new_status.capitalize()}"
            message = f"""
Hello {user.name},

Your complaint regarding "{complaint.waste_type}" has been marked as '{new_status}' by the collector.

Thank you for using our service.

Regards,
WasteYaan Support Team
"""
            # Step 4: Send mail
            send_notification_email(
                    from_mail="esmshelpline@gmail.com",
                    to_mail=user.email,
                    subject=subject,
                    message=message
                )

            # Step 5: Save to Notification model
            Notification.objects.create(
                to_mail=user.email,
                from_mail='esmshelpline@gmail.com',
                subject=subject,
                message=message
            )

            return Response({"message": f"Complaint status updated and email sent to {user.email}."}, status=200)

        except Exception as e:
            print("Exception:", str(e))
            return Response({"error": "Internal Server Error"}, status=500)