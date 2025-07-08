# users_panel/urls.py
from django.urls import path
from .views import UserDashboardDataView,SupervisorAreaListView,SupervisorCollectorListView,AssignCollectorToAreaView
from .views import SupervisorComplaintListView,SupervisorCollectorDataListView,AreaUserComplaintCountView
from .views import CollectorPickupCountView,CollectorTodayPickupView,CollectorPendingPickupView,CollectorCompletedPickupView
from .views import UserComplaintCountView,UserActiveComplaintView,CompletedComplaintsView


urlpatterns = [
    path('user/dashboard-data/', UserDashboardDataView.as_view(), name='user-dashboard-data'),
    path('user/supervisor-assigned-area/', SupervisorAreaListView.as_view(), name='supervisor-assigned-area-list'),
    path('user/collector-list/', SupervisorCollectorListView.as_view(), name='collector-list-under-sup'),
    path('user/area-assign-collector/', AssignCollectorToAreaView.as_view(), name='area-assign-collector'),
    path('user/supervisor-complaint-list/',SupervisorComplaintListView.as_view(), name='supervisor-complaint-list'),
    path('user/supervisor-collector-data/',SupervisorCollectorDataListView.as_view(), name='supervisor-collector-data'),
    path('user/supervisor-areas-user-list/',AreaUserComplaintCountView.as_view(), name='supervisor-areas-user-list'),
   
   
   
    path('user/collector-dash-pickup/',CollectorPickupCountView.as_view(), name='collector-dash-pickup'),
    path('user/collector-today-pickup/',CollectorTodayPickupView.as_view(), name='collector-today-pickup'),
    path('user/collector-pending-pickup/',CollectorPendingPickupView.as_view(), name='collector-pending-pickup'),
    path('user/collector-completed-pickup/',CollectorCompletedPickupView.as_view(), name='collector-completed-pickup'),


    path('user/dash-complaints-count/',UserComplaintCountView.as_view(), name='user-dash'),
    path('user/dash-active-complaints/',UserActiveComplaintView.as_view(), name='active-complaints'),
    path('user/dash-completed-complaints/',CompletedComplaintsView.as_view(), name='copleted-complaints'),
    
]
