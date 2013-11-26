from cookiejar import utils
from unittest import TestCase

import os


class UtilsTests(TestCase):
    def test_recursive_update(self):
        dict1 = {
            'a': {
                'a1': 1,
                'a2': 2
            },
            'b': {
                'b1': 3,
                'b2': 4
            }
        }
        dict2 = {
            'b': {
                'b2': 5
            }
        }

        expected = {
            'a': {
                'a1': 1,
                'a2': 2
            },
            'b': {
                'b1': 3,
                'b2': 5
            }
        }
        new_dict = utils.recursive_update(dict1, dict2)
        self.assertTrue('a' in new_dict)
        self.assertEqual(new_dict, expected)

    def test_clean_dict(self):
        dict1 = {
            'a': 1,
            'b': None,
            'c': {}
        }

        expected = {
            'a': 1
        }
        new_dict = utils.clean_dict(dict1)
        self.assertEqual(new_dict, expected)

    def test_convert_pathsep(self):
        s = """a/b/c"""
        expected = """a%sb%sc""" % (os.path.sep, os.path.sep)
        result = utils.convert_pathsep(s)
        self.assertEqual(result, expected)

    def test_is_remote(self):
        self.assertTrue(utils.is_remote('http://example.com'))
        self.assertTrue(utils.is_remote('https://example.com'))
        self.assertFalse(utils.is_remote('/home/httpd/'))
        self.assertFalse(utils.is_remote('/home//httpd/'))
