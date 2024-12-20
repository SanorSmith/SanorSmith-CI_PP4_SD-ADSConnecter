"""
Project views error handling test module
"""
# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd Party:
from django.test import SimpleTestCase, RequestFactory
from django.urls import reverse
from django.core.exceptions import SuspiciousOperation, PermissionDenied
from ads.views import handler500, handler403, handler404, trigger_400, trigger_403
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class TestErrorViews(SimpleTestCase):
    """
    Tests for error handling views in the project without touching the database.
    """

    def setUp(self):
        # Set up a factory to generate requests
        self.factory = RequestFactory()

    def test_handler500(self):
        """
        Test the custom 500 error handler.
        This will simulate a 500 error in the application.
        """
        request = self.factory.get('/trigger-500/')  # Trigger a 500 error
        response = handler500(request)
        self.assertEqual(response.status_code, 500)

    def test_handler403(self):
        """
        Test the custom 403 error handler.
        This will simulate a 403 error when a user is forbidden to access a page.
        """
        request = self.factory.get('/trigger-403/')  # Trigger a 403 error
        response = handler403(request)
        self.assertEqual(response.status_code, 403)

    def test_handler404(self):
        """
        Test the custom 404 error handler.
        This will simulate a 404 error when a page is not found.
        """
        request = self.factory.get('/non-existent-page/')  # Trigger a 404 error
        response = handler404(request)
        self.assertEqual(response.status_code, 404)

    def test_trigger_400(self):
        """
        Test if triggering a 400 error raises SuspiciousOperation.
        """
        request = self.factory.get('/trigger-400/')
        with self.assertRaises(SuspiciousOperation):
            trigger_400(request)

    def test_trigger_403_permission_denied(self):
        """
        Test if triggering a 403 error raises PermissionDenied.
        """
        request = self.factory.get('/trigger-403/')
        with self.assertRaises(PermissionDenied):
            trigger_403(request)
