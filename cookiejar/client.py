import json
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen
from .utils import cached_property


class ResultsIterator(object):
    idx = 0
    results = []

    def __init__(self, data):
        self.data = data
        self.results = data['results']
        return super(ResultsIterator, self).__init__()

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        try:
            item = self[self.idx]
        except IndexError:
            raise StopIteration()
        else:
            self.idx += 1
            return item

    def __getitem__(self, idx):
        try:
            return self.results[idx]
        except IndexError:
            if self.data['next'] is not None:
                self.fetch_next_page()
                return self[idx]
            else:
                raise

    def fetch_next_page(self):
        url = self.data['next']
        data = self.fetch(url)
        self.data = data
        self.results.extend(data['results'])

    def fetch(self, url):
        if url.startswith('http'):
            response = urlopen(url)
        else:
            response = open(url)
        return json.loads(response.read().decode('utf-8'))

    def __repr__(self):
        return self.results.__repr__()


class CookiejarClient(object):
    _data = None

    def __init__(self, index=None):
        from .settings import DEFAULTS

        if index is None:
            self.index = DEFAULTS['index']
        else:
            self.index = index

        super(CookiejarClient, self).__init__()

    def get_url(self):
        return self.index

    def fetch(self):
        if self.index.startswith('http'):
            response = urlopen(self.get_url())
        else:
            response = open(self.get_url())
        return json.loads(response.read().decode('utf-8'))


    @cached_property
    def data(self):
        return self.fetch()

    @cached_property
    def results(self):
        return ResultsIterator(self.data)
