from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Contacts, Advertisement
from .serializers import NotifyContactSerializer,NotificationContactSerializer



class AddContactView(APIView):
    def post(self, request):
        try:
            # Get data from the request body
            name = request.data.get("name")
            email = request.data.get("email")
            mobile = request.data.get("mobile")
            message = request.data.get("message")

            # Check if all required fields are provided
            if not (name and email and mobile and message):
                return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

            # Create a new contact record
            contact = Contacts.objects.create(
                name=name,
                email=email,
                mobile=mobile,
                message=message
            )
            contact.save()

            return Response({"message": "Contact added successfully!"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ListContactsView(APIView):
    def get(self, request):
        try:
            # Fetch all contact records
            contacts = Contacts.objects.all()
            serializer = NotifyContactSerializer(contacts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AddAdvertisementView(APIView):
    def post(self, request):
        try:
            advt_no = request.data.get('advt_no')
            title = request.data.get('title')
            description = request.data.get('description')
            file = request.FILES.get('file')

            # Check if all required fields are provided
            if not advt_no or not title or not description or not file:
                return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the advertisement number is unique
            if Advertisement.objects.filter(advt_no=advt_no).exists():
                return Response({'error': 'Advertisement number already exists.'}, status=status.HTTP_400_BAD_REQUEST)

            # Create and save the advertisement
            new_advt = Advertisement(
                advt_no=advt_no,
                title=title,
                description=description,
                file=file
            )
            new_advt.save()

            return Response({'message': 'Advertisement added successfully!'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class AdvertisementListView(APIView):
    def get(self, request):
        try:
            adverts = Advertisement.objects.all().order_by('-date')  # Latest first
            serializer = NotificationContactSerializer(adverts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)












