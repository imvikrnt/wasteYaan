from django.urls import path
from .views import AddContactView, ListContactsView,AddAdvertisementView,AdvertisementListView

urlpatterns = [
    path('add-contact/', AddContactView.as_view(), name='add_contact'),
    path('list-contacts/', ListContactsView.as_view(), name='list_contacts'),
    path('add/new-advertisement/', AddAdvertisementView.as_view(), name='new-advertisement'),
    path('get/advertisement/', AdvertisementListView.as_view(), name='get-advertisement'),
]
