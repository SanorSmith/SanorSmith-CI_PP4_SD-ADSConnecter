"""
URL configuration for servicetisement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.shortcuts import render
from ads import views as ads_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('ads.urls')),  
    path('trigger-400/', ads_views.trigger_400),
    path('trigger-403/', ads_views.trigger_403),
    path('trigger-500/', ads_views.trigger_500),
]

def custom_page_not_found(request, exception):
    return render(request, '404.html', status=404)

def custom_bad_request(request, exception):
    return render(request, '400.html', status=400)

def custom_permission_denied(request, exception):
    return render(request, '403.html', status=403)

def custom_server_error(request):
    return render(request, '500.html', status=500)

handler400 = 'servicetisement.urls.custom_bad_request'
handler403 = 'servicetisement.urls.custom_permission_denied'
handler404 = 'servicetisement.urls.custom_page_not_found'
handler500 = 'servicetisement.urls.custom_server_error'
