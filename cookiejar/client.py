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
    response = None
    results = []
    data_indexed = {}

    def __init__(self, data, client):
        self.data = data
        self.client = client
        self.add_results(data['results'])

        return super(ResultsIterator, self).__init__()

    def __iter__(self):
        return self

    def __getitem__(self, idx):
        try:
            return self.results[idx]
        except IndexError:
            if self.data['next']:
                self.fetch_next_page()
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
        self.results = self.data_indexed.values()
        self.results.sort(key=lambda x: x['id'])

    def fetch_next_page(self):
        url = self.data['next']
        response = self.client.fetch(url)
        self.data = response.data
        self.add_results(response.data['results'])

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

    def is_remote(self, url):
        return url.startswith('http')

    def fetch(self, url=None, **kwargs):
        if url is None:
            url = self.index

        if self.is_remote(url):
            url = "%s?%s" % (url, urlencode(kwargs))
            response = urlopen(url)
        else:
            response = open(url)

        data = json.load(response)
        results = ResultsIterator(data, client=self)
        if not self.is_remote(url):
            results.fetch_all_pages()
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
