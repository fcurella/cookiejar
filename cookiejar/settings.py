try:
    from ConfigParser import SafeConfigParser
except ImportError:
    from configparser import SafeConfigParser
import os

from .loaders import (
    URLLoader, FileSystemLoader, GitLoader, HgLoader, InstalledLoader
)
from .utils import clean_dict, recursive_update

from cookiecutter.config import get_user_config

COOKIECUTTER_CONFIG = get_user_config()

DEFAULTS = {
    'support_dir': os.path.expanduser('~/.cookiejar'),
    'config_file': os.path.expanduser('~/.cookiejar/cookiejarrc'),
    'index': 'https://raw.github.com/fcurella/cookiejar-channel/master/index.json',
    'template-loaders': (
        URLLoader,
        GitLoader,
        HgLoader,
        FileSystemLoader,
        InstalledLoader,
    ),
    'templates_dir': os.path.join(COOKIECUTTER_CONFIG['cookiecutters_dir'], ''),
}



class RecursiveDict(dict):
    def recursive_update(self, kwargs):
        self = recursive_update(self, clean_dict(kwargs))
        return self


class SettingsLoader(RecursiveDict):
    def parse(self, config_file):
        kwargs = {}
        parser = SafeConfigParser()

        if os.path.exists(config_file):
            with open(config_file) as fh:
                parser.readfp(fh)

            for section in parser.sections():
                kwargs[section] = recursive_update(kwargs.get(section, {}), dict(parser.items(section)))

        return kwargs


class DefaultsLoader(SettingsLoader):
    def __init__(self):
        super(DefaultsLoader, self).__init__(**DEFAULTS)


class UserSettingLoader(SettingsLoader):
    config_file = DEFAULTS['config_file']

    def __init__(self, config_file=None):
        if config_file is not None:
            self.config_file = config_file

        kwargs = self.parse(self.config_file)

        super(UserSettingLoader, self).__init__(**kwargs)


class CommandLineSettingLoader(SettingsLoader):
    pass


class SettingsReader(dict):
    support_dir = DEFAULTS['support_dir']

    def __init__(self, config_file=None, *args, **kwargs):
        _kwargs = RecursiveDict()

        defaults = DefaultsLoader()
        command_line = CommandLineSettingLoader(**kwargs)
        user = UserSettingLoader(config_file)

        _kwargs.recursive_update(defaults)
        _kwargs.recursive_update(user)
        _kwargs.recursive_update(command_line)

        super(SettingsReader, self).__init__(**_kwargs)
