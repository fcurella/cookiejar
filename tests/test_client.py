import os
from unittest import TestCase

from cookiejar.client import CookiejarClient


class ClientTests(TestCase):
    maxDiff = None
    def test_pagination(self):
        index = os.path.join((os.path.dirname(os.path.abspath(__file__))), 'index.1.json')
        
        client = CookiejarClient(index=index)

        expected = [
            {
                u'id': 1,
                u'name': u'audreyr/pypackage',
                u'url': u'https://github.com/audreyr/cookiecutter-pypackage/archive/fe165c5242cc889db0c58476abde905cecf14dfa.zip',
                u'version': u'0.0.1',
                u'author': u'Audrey Roy',
                u'description': u'Cookiecutter template for a Python package.',
                u'checksum': "md5$a79cc0ef3897d14eeb3b5be6a37a5ff8",
                u'user': u'audreyr',
            },
            {
                u'id': 2,
                u'name': u'sloria/flask',
                u'url': u'https://github.com/sloria/cookiecutter-flask/archive/97e835461d31c00e9f16ac79ef3af9aeb13ae84a.zip',
                u'version': u'0.0.1',
                u'author': u'Steven Loria',
                u'description': u'A flask template with Twitter Bootstrap 3, starter templates, and basic registration/authentication.',
                u'checksum': "md5$72aa94d5768756231c66d8ce03ca51cc",
                u'user': u'sloria',
            },
            {
                u'id': 3,
                u'name': u'pydanny/django',
                u'url': u'https://github.com/pydanny/cookiecutter-django/archive/172036f8f34b82c29bdc0bb3f31f5b703d0ce8f8.zip',
                u'version': u'0.0.1',
                u'author': u'Daniel Greenfeld',
                u'description': u'A cookiecutter template for creating reusable Django projects quickly.',
                u'checksum': "md5$874ce3c00faabde6a11fb3c9d3909649",
                u'user': u'pydanny',
            }
        ]
        results = client.filter()
        res = list(results)
        self.assertEqual(len(res), len(expected))
        self.assertEqual(res, expected)

    def test_get(self):
        index = os.path.join((os.path.dirname(os.path.abspath(__file__))), 'index.1.json')
        
        client = CookiejarClient(index=index)

        expected = {
            u'id': 2,
            u'name': u'sloria/flask',
            u'url': u'https://github.com/sloria/cookiecutter-flask/archive/97e835461d31c00e9f16ac79ef3af9aeb13ae84a.zip',
            u'version': u'0.0.1',
            u'author': u'Steven Loria',
            u'description': u'A flask template with Twitter Bootstrap 3, starter templates, and basic registration/authentication.',
            u'checksum': "md5$72aa94d5768756231c66d8ce03ca51cc",
            u'user': u'sloria',
        }
        client.fetch()
        result = client.get('sloria/flask')
        self.assertEqual(result, expected)
        self.assertRaises(RuntimeError, client.get, 'unexisting_tmeplate')
