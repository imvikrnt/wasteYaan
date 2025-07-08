from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models import User  
from django.db.models import Count
from django.shortcuts import get_object_or_404
from admin_panel.models import Area, CollectorAssign
from waste_management.models import Complaint
from django.utils.timezone import now

class UserDashboardDataView(APIView):
    def get(self, request):
        id = request.query_params.get('id')
        print("usersdashid",id)
        try:
            # Fetching user details
            if not id:
                return Response({"error": "Missing ID"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = get_object_or_404(User, id=id)
            except:
                return Response({"error": "Invalid User ID"}, status=status.HTTP_400_BAD_REQUEST)

            user_data = {
                'role': user.role,
                'name': user.name,
                'profile_img': user.profile_img.url if user.profile_img else None,
            }

            # Counting areas assigned to the user (as supervisor)
            area_count = Area.objects.filter(supervisorassigned=user).count()

            # Counting collectors assigned under the supervisor
            collector_count = CollectorAssign.objects.filter(supervisorassigned=user).count()

            # Counting complaints in areas supervised by the user
            area_ids = Area.objects.filter(supervisorassigned=user).values_list('id', flat=True)
            complaint_count = Complaint.objects.filter(area__in=area_ids).count()

            # Preparing the response data
            response_data = {
                'user_data': user_data,
                'area_count': area_count,
                'collector_count': collector_count,
                'complaint_count': complaint_count,
            }
            print(response_data)
            return Response(response_data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SupervisorAreaListView(APIView):
    def get(self, request):
        try:
            # Fetching supervisor ID from query parameters
            supervisor_id = request.query_params.get('id')
            if not supervisor_id:
                return Response({'error': 'Supervisor ID not provided'}, status=status.HTTP_400_BAD_REQUEST)

            # Fetching supervisor details
            supervisor = User.objects.get(id=supervisor_id, role='supervisor')

            # Counting and listing areas assigned to the supervisor
            assigned_areas = Area.objects.filter(supervisorassigned=supervisor)
            area_count = assigned_areas.count()
            # area_list = list(assigned_areas.values_list('area_name', flat=True))
            area_list = list(assigned_areas.values('id', 'area_name'))

            # Preparing the response data
            response_data = {
                'area_count': area_count,
                'area_list': area_list,
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'Supervisor not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SupervisorCollectorListView(APIView):
    def get(self, request):
        try:
            # Fetching supervisor ID from query parameters
            supervisor_id = request.query_params.get('id')
            if not supervisor_id:
                return Response({'error': 'Supervisor ID not provided'}, status=status.HTTP_400_BAD_REQUEST)

            # Fetching supervisor details
            supervisor = User.objects.get(id=supervisor_id, role='supervisor')

            # Collectors assigned to the supervisor
            assigned_collectors = CollectorAssign.objects.filter(supervisorassigned=supervisor)
            collector_list = [
                {
                    'id': collector.collectorassigned.id,
                    'name': collector.collectorassigned.name,
                    'user_id': collector.collectorassigned.user_id,
                 
                }
                for collector in assigned_collectors if collector.collectorassigned
            ]
            collector_count = len(collector_list)

            # Preparing the response data
            response_data = {
                'collector_count': collector_count,
                'collector_list': collector_list,
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'Supervisor not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AssignCollectorToAreaView(APIView):
    def post(self, request):
        try:
            supervisor_id = request.data.get('supervisor_id')
            collector_id = request.data.get('collector_id')
            area_id = request.data.get('area_id')

            if not (supervisor_id and collector_id and area_id):
                return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

            supervisor = User.objects.get(id=supervisor_id, role='supervisor')
            collector = User.objects.get(id=collector_id, role='collector')
            area = Area.objects.get(id=area_id)

            # Validation 1: Check if the area is assigned to the given supervisor
            if area.supervisorassigned != supervisor:
                return Response({'error': 'Supervisor not assigned to this area'}, status=status.HTTP_403_FORBIDDEN)

            # Validation 2: Check if the area is already assigned to another collector
            if area.collectorassigned and area.collectorassigned != collector:
                return Response({'error': 'Already assigned to another collector'}, status=status.HTTP_400_BAD_REQUEST)

            area.collectorassigned = collector
            area.is_assigned = True
            area.save()

            # Update CollectorAssign table
            CollectorAssign.objects.update_or_create(
                supervisorassigned=supervisor, collectorassigned=collector, defaults={'is_assigned': True}
            )

            return Response({'success': 'Collector assigned to area successfully'}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Area.DoesNotExist:
            return Response({'error': 'Area not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Area.DoesNotExist:
            return Response({'error': 'Area not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SupervisorComplaintListView(APIView):
    def get(self, request):
        try:
            supervisor_id = request.query_params.get('id')
            if not supervisor_id:
                return Response({'error': 'Supervisor ID not provided'}, status=status.HTTP_400_BAD_REQUEST)

            supervisor = User.objects.get(id=supervisor_id, role='supervisor')
            assigned_areas = Area.objects.filter(supervisorassigned=supervisor)
            area_names = list(assigned_areas.values_list('area_name', flat=True))

            complaints = Complaint.objects.filter(area__in=area_names)
            complaint_list = []

            for complaint in complaints:
                # Find the assigned collector for the complaint's area
                assigned_collector = Area.objects.filter(area_name=complaint.area).values_list('collectorassigned__user_id', flat=True).first()

                complaint_list.append({
                    'id': complaint.id,
                    'user': complaint.user.name,
                    'user_id': complaint.user.user_id,
                    'waste_type': complaint.waste_type,
                    'description': complaint.description,
                    'address': complaint.address,
                    'area': complaint.area,
                    'status': complaint.status,
                    'date': complaint.date,
                    'assigned_collector_id': assigned_collector if assigned_collector else 'N/A',
                })

            response_data = {
                'supervisor_id': supervisor_id,
                'complaint_count': len(complaint_list),
                'complaint_list': complaint_list,
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'Supervisor not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        except User.DoesNotExist:
            return Response({'error': 'Supervisor not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SupervisorCollectorDataListView(APIView):
    def get(self, request):
        try:
            supervisor_id = request.query_params.get('id')
            if not supervisor_id:
                return Response({'error': 'Supervisor ID not provided'}, status=status.HTTP_400_BAD_REQUEST)

            supervisor = User.objects.get(id=supervisor_id, role='supervisor')
            collectors = CollectorAssign.objects.filter(supervisorassigned=supervisor)

            collector_list = []
            for collector in collectors:
                collector_details = {
                    'id': collector.collectorassigned.id,
                    'role': collector.collectorassigned.role,
                    'user_id': collector.collectorassigned.user_id,
                    'name': collector.collectorassigned.name,
                    'email': collector.collectorassigned.email,
                    'mobile': collector.collectorassigned.mobile,
                    'dob': collector.collectorassigned.dob,
                    'gender': collector.collectorassigned.gender,
                    'nationality': collector.collectorassigned.nationality,
                    'is_active': collector.collectorassigned.is_active,
                }
                collector_list.append(collector_details)

            response_data = {
                'supervisor_id': supervisor_id,
                'collector_count': len(collector_list),
                'collectors': collector_list,
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'Supervisor not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AreaUserComplaintCountView(APIView):
    def get(self, request):
        try:
            supervisor_id = request.query_params.get('id')
            if not supervisor_id:
                return Response({'error': 'Supervisor ID not provided'}, status=status.HTTP_400_BAD_REQUEST)

            supervisor = User.objects.get(id=supervisor_id, role='supervisor')
            assigned_areas = Area.objects.filter(supervisorassigned=supervisor)
            area_names = list(assigned_areas.values_list('area_name', flat=True))

            users = Complaint.objects.filter(area__in=area_names).values('user').annotate(count=Count('id'))
            user_list = []

            for user in users:
                user_info = User.objects.get(id=user['user'])
                user_list.append({
                    'user_id': user_info.user_id,
                    'name': user_info.name,
                    'dob': user_info.dob,
                    'gender': user_info.gender,
                    'mobile': user_info.mobile,
                    'email': user_info.email,
                    'nationality': user_info.nationality,
                    'is_active': user_info.is_active,
                    'complaint_count': user['count'],
                })

            response_data = {
                'supervisor_id': supervisor_id,
                'user_complaint_count': user_list,
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'Supervisor not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#COLLECTOR VIEWS
class CollectorPickupCountView(APIView):
    def get(self, request):
        try:
            collector_id = request.query_params.get('id')
            if not collector_id:
                return Response({'error': 'Collector ID not provided'}, status=status.HTTP_400_BAD_REQUEST)

            collector = User.objects.get(id=collector_id, role='collector')

            # Get areas assigned to the collector
            assigned_areas = Area.objects.filter(collectorassigned=collector)
            area_names = list(assigned_areas.values_list('area_name', flat=True))

            # Today's date
            today = now().date()

            # Fetching Today's Pickups
            todays_pickups_count = Complaint.objects.filter(area__in=area_names, date__date=today).count()

            # Fetching Completed Pickups
            completed_pickups_count = Complaint.objects.filter(area__in=area_names, status='resolved').count()

            # Fetching Pending Areas
            pending_areas_count = Complaint.objects.filter(area__in=area_names).exclude(status='resolved').count()

            response_data = {
                'todays_pickups_count': todays_pickups_count,
                'completed_pickups_count': completed_pickups_count,
                'pending_areas_count': pending_areas_count,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'Collector not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 

class CollectorTodayPickupView(APIView):
    def get(self, request):
        try:
            collector_id = request.query_params.get('id')
            if not collector_id:
                return Response({'error': 'Collector ID not provided'}, status=status.HTTP_400_BAD_REQUEST)

            collector = User.objects.get(id=collector_id, role='collector')

            # Get areas assigned to the collector
            assigned_areas = Area.objects.filter(collectorassigned=collector)
            area_names = list(assigned_areas.values_list('area_name', flat=True))

            # Today's date
            today = now().date()

            # Fetching Today's Pickups
            todays_pickups = Complaint.objects.filter(area__in=area_names, date__date=today)
            if not todays_pickups.exists():
                todays_pickups_list = ['Today, there are no complaints.']
            else:
                todays_pickups_list = []
                for p in todays_pickups:
                    user_details = {
                        'user_id': p.user.user_id,
                        'name': p.user.name,
                        'email': p.user.email,
                        'address': p.address,
                        'mobile': p.user.mobile,
                    }
                    pickup_info = {
                        'id': p.id,
                        'area': p.area,
                        'status': p.status,
                        'date': p.date,
                        'user': user_details,
                    }
                    todays_pickups_list.append(pickup_info)

            response_data = {
                'todays_pickups': todays_pickups_list,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'Collector not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CollectorPendingPickupView(APIView):
    def get(self, request):
        try:
            collector_id = request.query_params.get('id')
            if not collector_id:
                return Response({'error': 'Collector ID not provided'}, status=status.HTTP_400_BAD_REQUEST)

            collector = User.objects.get(id=collector_id, role='collector')

            # Get areas assigned to the collector
            assigned_areas = Area.objects.filter(collectorassigned=collector)
            area_names = list(assigned_areas.values_list('area_name', flat=True))

            # Fetching Pending Pickups
            # pending_pickups = Complaint.objects.filter(area__in=area_names, status='pending')
            pending_pickups = Complaint.objects.filter(area__in=area_names).exclude(status='resolved')
            if not pending_pickups.exists():
                pending_pickups_list = ['No pending pickups.']
            else:
                pending_pickups_list = []
                for p in pending_pickups:
                    user_details = {
                        'user_id': p.user.user_id,
                        'name': p.user.name,
                        'email': p.user.email,
                        'address': p.address,
                        'mobile': p.user.mobile,
                    }
                    pickup_info = {
                        'id': p.id,
                        'area': p.area,
                        'status': p.status,
                        'date': p.date,
                        'user': user_details,
                    }
                    pending_pickups_list.append(pickup_info)

            response_data = {
                'pending_pickups': pending_pickups_list,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'Collector not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        except User.DoesNotExist:
            return Response({'error': 'Collector not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        except User.DoesNotExist:
            return Response({'error': 'Collector not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CollectorCompletedPickupView(APIView):
    def get(self, request):
        try:
            collector_id = request.query_params.get('id')
            if not collector_id:
                return Response({'error': 'Collector ID not provided'}, status=status.HTTP_400_BAD_REQUEST)

            collector = User.objects.get(id=collector_id, role='collector')

            # Get areas assigned to the collector
            assigned_areas = Area.objects.filter(collectorassigned=collector)
            area_names = list(assigned_areas.values_list('area_name', flat=True))

            # Fetching Completed Pickups
            completed_pickups = Complaint.objects.filter(area__in=area_names, status='resolved')
            if not completed_pickups.exists():
                completed_pickups_list = ['No completed pickups.']
            else:
                completed_pickups_list = []
                for p in completed_pickups:
                    user_details = {
                        'user_id': p.user.user_id,
                        'name': p.user.name,
                        'email': p.user.email,
                        'address': p.address,
                        'mobile': p.user.mobile,
                    }
                    pickup_info = {
                        'id': p.id,
                        'area': p.area,
                        'status': p.status,
                        'date': p.date,
                        'user': user_details,
                    }
                    completed_pickups_list.append(pickup_info)

            response_data = {
                'completed_pickups': completed_pickups_list,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'Collector not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# individual users
class UserComplaintCountView(APIView):
    def get(self, request):
        try:
            user_id = request.query_params.get('id')
            if not user_id:
                return Response({'error': 'User ID not provided'}, status=status.HTTP_400_BAD_REQUEST)

            completed_count = Complaint.objects.filter(user_id=user_id, status='resolved').count()
            active_count = Complaint.objects.filter(user_id=user_id).exclude(status='resolved').count()

            response_data = {
                'completed_count': completed_count,
                'active_count': active_count,
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserActiveComplaintView(APIView):
    def get(self, request):
        try:
            user_id = request.query_params.get('id')
            if not user_id:
                return Response({'error': 'User ID not provided'}, status=status.HTTP_400_BAD_REQUEST)

            active_complaints = Complaint.objects.filter(user_id=user_id).exclude(status='resolved')
            active_complaints_list = []
            for complaint in active_complaints:
                complaint_data = {
                    'id': complaint.id,
                    'area': complaint.area,
                    'status': complaint.status,
                    'date': complaint.date,
                    'description': complaint.description,
                    'image': complaint.waste_image.url if complaint.waste_image else None,
                }
                active_complaints_list.append(complaint_data)

            return Response({'active_complaints': active_complaints_list}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CompletedComplaintsView(APIView):
    def get(self, request):
        try:
            user_id = request.query_params.get('id')
            if not user_id:
                return Response({'error': 'User ID not provided'}, status=status.HTTP_400_BAD_REQUEST)

            completed_complaints = Complaint.objects.filter(user_id=user_id, status='resolved')
            completed_complaints_list = []
            for complaint in completed_complaints:
                complaint_data = {
                    'id': complaint.id,
                    'area': complaint.area,
                    'status': complaint.status,
                    'date': complaint.date,
                    'description': complaint.description,
                    'image': complaint.waste_image.url if complaint.waste_image else None,
                }
                completed_complaints_list.append(complaint_data)

            return Response({'completed_complaints': completed_complaints_list}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)










