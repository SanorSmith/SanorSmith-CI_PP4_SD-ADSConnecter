# update_cloudinary_css.py
import os
import django
import cloudinary
import cloudinary.api
import cloudinary.uploader

if os.path.isfile('env.py'):
    import env
# Ensure Cloudinary is configured
cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET')
)

try:
    # Upload updated CSS file
    upload_result = cloudinary.uploader.upload(
        "static/css/styles.css",
        public_id="static/css/styles",  # Adjust path if needed
        resource_type="raw",
        invalidate=True  # This will ensure Cloudinary cache is invalidated
    )
    print("CSS file successfully updated:", upload_result)
except Exception as e:
    print("Error updating CSS file in Cloudinary:", e)
