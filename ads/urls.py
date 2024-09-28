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
    path('profile/', views.profile, name='profile'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('add-service-form/', views.add_service_form, name='add_service_form'),
    path('edit-service-form/<int:service_id>/', views.edit_service_form, name='edit_service_form'),
]