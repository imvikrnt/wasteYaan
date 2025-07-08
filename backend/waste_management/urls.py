from django.urls import path
from .views import CreateComplaintView, AssignCollectorView,ComplaintListView,UpdatePickupStatusView

urlpatterns = [
    path('user/create-complaint/', CreateComplaintView.as_view(), name='create_complaint'),
    path('complaint-list/', ComplaintListView.as_view(), name='get-complaint-list'),
    path('complaint/<int:complaint_id>/assign-collector/', AssignCollectorView.as_view(), name='assign_collector'),
    path('complaint/update-pickup-status/<int:pickup_id>', UpdatePickupStatusView.as_view(), name='update-pickup-status'),
]
