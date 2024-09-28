from django.conf import settings

def cloudinary_static_url(request):
    return {
        'CLOUDINARY_STATIC_URL': settings.CLOUDINARY_STATIC_URL
    }
