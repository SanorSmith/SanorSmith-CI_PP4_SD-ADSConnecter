from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('sign-in/', views.sign_in, name='sign_in'),
    path('sign-out/', views.sign_out, name='sign_out'),
    path('available-services/', views.available_services, name='available_services'),
    path('add-service/', views.add_service, name='add_service'),
    path('update-service/<int:service_id>/', views.update_service, name='update_service'),
    path('remove-service/<int:service_id>/', views.remove_service, name='remove_service'),
    path('operations/', views.operations, name='operations'),
]