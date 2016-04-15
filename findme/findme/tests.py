from django.test import TestCase
from django.test.client import RequestFactory

from project import urls

from ..views import handler404, handler500


class TestErrorPages(TestCase):

    def test_error_handlers(self):
        self.assertTrue(urls.handler404.endswith('.handler404'))
        factory = RequestFactory()
        request = factory.get('/')
        response = handler404(request)
        self.assertEqual(response.status_code, 404)
        self.assertIn('404 Not Found!!', unicode(response))