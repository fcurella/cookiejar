from .settings import SettingsReader
from .creator import PackageCreator
from .channel import Channel


class Jar(object):
    def __init__(self):
        self.settings = SettingsReader()
        super(Jar, self).__init__()

    def run(self, action, **kwargs):
        return getattr(self, action)(**kwargs)

    def create(self, template_name, context):
        creator = PackageCreator(settings=self.settings)
        creator.create(template_name, context)

    def installed(self):
        channel = Channel(settings=self.settings)
        channel.installed()

    def list(self, index=None):
        channel = Channel(settings=self.settings, index=index)
        channel.list()

    def search(self, text, index=None):
        channel = Channel(settings=self.settings, index=index)
        channel.search(text)

    def add(self, template_name, url=None, index=None):
        channel = Channel(settings=self.settings, index=index)
        channel.add(template_name, url)

    def remove(self, template_name):
        channel = Channel(settings=self.settings)
        channel.remove(template_name)
