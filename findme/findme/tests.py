from django.test import TestCase, SimpleTestCase
from django.test.client import RequestFactory

from findme import urls

from .views import handler404

from pip.req import parse_requirements
import pkg_resources


class TestErrorPages(TestCase):

    def test_error_handlers(self):
        self.assertTrue(urls.handler404.endswith('.handler404'))
        factory = RequestFactory()
        request = factory.get('/')
        response = handler404(request)
        self.assertEqual(response.status_code, 404)
        self.assertIn('404 Not Found!!', unicode(response))


#from 10 self service
class TestRequirements(SimpleTestCase):

    ignore = set((
        'argparse',
        'pip',
        'wheel',
        'wsgiref',
        'setuptools',
    ))

    def test_no_pip_freeze_mishaps(self):
        # See https://caremad.io/2013/07/setup-vs-requirement/
        # We are trying to stop:
        # - 'pip freeze' leaking things we don't actually depend on into
        #   requirements.txt (think pip-tools etc)
        # - Removing a dependency from requirements but not its own
        #   dependencies - for example, if we removed django-redis we might
        #   want to remove redis

        requirements = parse_requirements('requirements.txt', session=self.requests.Session())
        packages_a = set(p.name for p in requirements) - self.ignore

        setup_py = pkg_resources.require('ten-self-service[test,docs]')
        packages_b = set(p.project_name for p in setup_py) - self.ignore

        # Separate assertions so that we can easily see whats wrong - checking
        # equality would work but wouldn't tell us what was wrong

        # Check for packages in setup.py but not requirements.txt
        # If you are adding a new dep, you might need to 'pip freeze'
        # If you are removing a dep, you forgot to remove it from setup.py
        self.assertEqual(packages_b - packages_a, set())

        # Check for packages in requirements.txt but not setup.py
        # If you are adding a new dep, add the *direct dependency* to setup.py.
        #    E.g. if you added django-redis to a project you would end up
        #    adding django-redis to setup.py and django-redis and redis to
        #    requirements.txt
        # If you are removing a dep, you forgot to remove it from requirements
        self.assertEqual(packages_a - packages_b, set())


class TestManage(TestCase):

    def test_main(self):
        manage.main(["--help"])


class TestCase(test.TestCase):

    @classmethod
    def flush_cache(cls):
        cache.clear()