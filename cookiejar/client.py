import json

try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode


class ResultsIterator(object):
    idx = 0
    results = []
    data_indexed = {}

    def __init__(self, data, client):
        self.data = data
        self.client = client
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
            self.idx = 0
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
        data = self.client.fetch(url)
        self.data = data
        self.results.extend(data['results'])

        indexed = dict([(result['name'], result) for result in data['results']])
        self.data_indexed.update(indexed)

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

    def is_remote(self, url):
        return url.startswith('http')

    def fetch(self, url):
        if url is None:
            url = self.index

        if self.is_remote(url):
            response = urlopen(url)
        else:
            response = open(url)

        data = json.loads(response.read().decode('utf-8'))
        return ResultsIterator(data, client=self)

    def filter(self, **kwargs):
        if self.is_remote(self.index):
            url = "%s?%s" % (self.index, urlencode(kwargs))
            return self.fetch(url)

        results = []
        for result in self.fetch(self.index):

            include = True

            for k, v in kwargs.items():
                if result[k].lower() != v.lower():
                    include = False
                    break

            if include:
                results.append(result)

        return results

    def search(self, text):
        return self.filter(name=text)

    def get(self, template_name):
        results = self.search(template_name)
        if template_name not in results.data_indexed:
            raise RuntimeError("Template '%s' not found." % template_name)
        return self.results.data_indexed[template_name]

