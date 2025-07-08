from django.urls import path
from .views import AdminDashboardDataView,AdminProfileDataView,UserRoleListView,WasteComplaintListView,UserUpdateActivityStatusView
from .views import AddAreaView,SupervisorAreaListView,UpdateAsignAreaSupervisorView,CollectorAssignView

urlpatterns = [
    path('admin/dashboard-data/', AdminDashboardDataView.as_view(), name='admin-dashboard-data'),
    path('admin/personal-data/', AdminProfileDataView.as_view(), name='admin-profile-data'),
    path('admin/users-data/', UserRoleListView.as_view(), name='admin-users-data'),
    path('admin/wastecomplaint-data/', WasteComplaintListView.as_view(), name='admin-wastecomplaint-data'),
    path('admin/update/user-activity-status/', UserUpdateActivityStatusView.as_view(), name='user-activity-status'),
   
   
    # area url here
    path('admin/add-area', AddAreaView.as_view(), name='add-area'),
    path('admin/supervisors-areas/', SupervisorAreaListView.as_view(), name='supervisor_area_list'),
    path('admin/assign-to-supervisor/', UpdateAsignAreaSupervisorView.as_view(), name='supervisor_area_assigned'),
    path('admin/assign-collector/', CollectorAssignView.as_view(), name='supervisor_collector_assigned'),

]