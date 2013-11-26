import os
import shutil
from unittest import TestCase

from cookiejar.channel import Channel
from cookiejar.settings import SettingsReader


class ChannelTests(TestCase):
    def test_add(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        config_path = os.path.join(current_dir, 'cookiejarrc')
        settings = SettingsReader(config_file=config_path)
        settings['templates_dir'] = os.path.join(current_dir, 'cookiecutters')
        index = os.path.join((os.path.dirname(os.path.abspath(__file__))), 'index.1.json')

        channel = Channel(settings=settings, index=index)
        channel.add("audreyr/pypackage")
        destination_path = os.path.join(settings['templates_dir'], 'audreyr', 'pypackage')
        self.assertTrue(os.path.exists(destination_path))
        destination_path = os.path.join(destination_path, 'cookiecutter.json')
        self.assertTrue(os.path.exists(destination_path))
        
        channel.remove("audreyr/pypackage")
        destination_path = os.path.join(settings['templates_dir'], 'audreyr', 'pypackage')
        self.assertFalse(os.path.exists(destination_path))
        shutil.rmtree(settings['templates_dir'])
