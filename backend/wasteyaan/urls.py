"""
URL configuration for wasteyaan project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),

    # path('api/user/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/user/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    
    #APP URLS
    path('api/', include('api.urls')),
    path('api/waste/', include('waste_management.urls')),
    path('api/admin-panel/', include('admin_panel.urls')),
    path('api/users-panel/', include('users_panel.urls')),
    path('api/notifycontact/', include('notifycontact.urls')),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)