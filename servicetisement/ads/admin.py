from django.contrib import admin
from .models import UserProfile, Service, ServiceCategory

admin.site.register(UserProfile)
admin.site.register(Service)
admin.site.register(ServiceCategory)