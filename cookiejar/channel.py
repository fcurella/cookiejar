from __future__ import absolute_import
import os
import shutil

from .extractor import PackageExtractor
from .client import CookiejarClient
from .utils import cached_property
from .pager import Pager


class Channel(object):
    _data = None

    def __init__(self, settings, index=None):
        self.client = CookiejarClient(index=index)
        self.templates_dir = settings['templates_dir']

        if not os.path.exists(self.templates_dir):
            os.makedirs(self.templates_dir)
        self.pager = Pager()
        super(Channel, self).__init__()

    def page(self, *args, **kwargs):
        self.pager.page(*args, **kwargs)

    def echo(self, *args, **kwargs):
        self.pager.echo(*args, **kwargs)

    @property
    def results(self):
        return self.client.results

    @cached_property
    def data_indexed(self):
        return dict([(result['name'], result) for result in self.results])

    @property
    def installed_list(self):
        templates = [d for d in os.listdir(self.templates_dir) if os.path.isdir(os.path.join(self.templates_dir, d))]
        templates.sort()
        return templates

    def installed(self):
        content = self.installed_list
        content.append("%d templates installed." % len(self.installed_list))
        self.page(content)

    def template_info(self, template_info):
        return "%s v%s %s" % (template_info['name'], template_info['version'], template_info['author'])

    def list(self):
        # TODO: Use an actual API
        self.page([self.template_info(result) for result in self.results])

    def search(self, text):
        # TODO: Use an actual API
        content = [self.template_info(result) for result in self.results if text in result['name']]
        self.page(content)

    def template_path(self, template_name):
        return os.path.join(self.templates_dir, template_name)

    def template_data(self, template_name):
        if template_name not in self.data_indexed:
            raise RuntimeError("Template '%s' not found." % template_name)
        return self.data_indexed[template_name]

    def template_url(self, template_name):
        return self.template_data(template_name)['url']

    def template_version(self, template_name):
        return self.template_data(template_name)['version']

    def template_author(self, template_name):
        return self.template_data(template_name)['author']

    def add(self, template_name, url=None):
        if url is None:
            url = self.template_url(template_name)
        destination = self.templates_dir
        extractor = PackageExtractor(url=url, template_name=template_name)
        extractor.extract(destination)

    def remove(self, template_name):
        template_dir = os.path.join(self.templates_dir, template_name)
        if os.path.exists(template_dir):
            shutil.rmtree(template_dir)
        else:
            self.echo("Template '%s' is not installed.\r\n" % template_name)
