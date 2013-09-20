import os
from unittest import TestCase

from cookiejar.settings import SettingsReader


class OptionsTests(TestCase):
    def test_read_configfile(self):
        config_path = os.path.join((os.path.dirname(os.path.abspath(__file__))), 'cookiejarrc')
        settings = SettingsReader(config_file=config_path)

        self.assertEqual(settings['author']['name'], 'John Smith')

        settings = SettingsReader(config_file=config_path, author={'name': 'John Brown'})
        self.assertEqual(settings['author']['name'], 'John Brown')
        self.assertTrue('email' in settings['author'])
