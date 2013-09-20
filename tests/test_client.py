import os
from unittest import TestCase

from cookiejar.client import CookiejarClient


class ClientTests(TestCase):
    def test_pagination(self):
        index = os.path.join((os.path.dirname(os.path.abspath(__file__))), 'index.1.json')
        
        client = CookiejarClient(index=index)

        expected = [{u'description': u'Cookiecutter template for a Python package.', u'author': u'Audrey Roy', u'url': u'https://github.com/audreyr/cookiecutter-pypackage/archive/master.zip', u'checksum': None, u'version': u'0.0.1', u'user': u'audreyr', u'pk': 1, u'name': u'pypackage'}, {u'description': u'A flask template with Twitter Bootstrap 3, starter templates, and basic registration/authentication.', u'author': u'Steven Loria', u'url': u'https://github.com/sloria/cookiecutter-flask/archive/master.zip', u'checksum': None, u'version': u'0.0.1', u'user': u'sloria', u'pk': 2, u'name': u'flask'}, {u'description': u'A cookiecutter template for creating reusable Django projects quickly.', u'author': u'Daniel Greenfeld', u'url': u'https://github.com/pydanny/cookiecutter-django/archive/master.zip', u'checksum': None, u'version': u'0.0.1', u'user': u'pydanny', u'pk': 3, u'name': u'django'}]
        results = client.results
        self.assertEqual([r for r in results], expected)
        self.assertEqual(results[0], expected[0])
        self.assertEqual(results[1:2], expected[1:2])
        with self.assertRaises(IndexError):
            results[3]
