import json

try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from .utils import is_remote


class ResultsIterator(object):
    idx = 0
    response = None
    results = []
    data_indexed = {}

    def __init__(self, url):
        self.fetch_page(url)

        if not is_remote(url):
            self.fetch_all_pages()

        return super(ResultsIterator, self).__init__()

    def __iter__(self):
        return self

    def __getitem__(self, idx):
        try:
            return self.results[idx]
        except IndexError:
            if self.data['next']:
                self.fetch_page(url=self.data['next'])
                return self.results[idx]
            else:
                raise

    def __next__(self):
        return self.next()

    def next(self):
        try:
            item = self[self.idx]
        except IndexError:
            self.idx = 0
            raise StopIteration()
        else:
            self.idx += 1
            return item

    def add_results(self, results):
        for result in results:
            self.data_indexed[result['name']] = result
        self.results = list(self.data_indexed.values())
        self.results.sort(key=lambda x: x['id'])

    def fetch_page(self, url):
        if is_remote(url):
            response = urlopen(url)
        else:
            response = open(url)

        data = json.load(response)
        self.data = data
        self.add_results(data['results'])

    def fetch_all_pages(self):
        list(self)


class CookiejarClient(object):
    def __init__(self, index=None):
        from .settings import DEFAULTS

        if index is None:
            self.index = DEFAULTS['index']
        else:
            self.index = index

        super(CookiejarClient, self).__init__()

    def fetch(self, url=None, **kwargs):
        if url is None:
            url = self.index

        if is_remote(url):
            url = "%s?%s" % (url, urlencode(kwargs))

        results = ResultsIterator(url)
        return results

    def filter(self, url=None, **kwargs):
        return self.fetch(url, **kwargs)

    def search(self, text):
        return self.filter(name=text)

    def get(self, template_name):
        results = self.search(template_name)
        if template_name not in results.data_indexed:
            raise RuntimeError("Template '%s' not found." % template_name)
        return results.data_indexed[template_name]
