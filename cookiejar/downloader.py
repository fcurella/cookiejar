try:
    from StringIO import StringIO
except ImportError:
    from io import BytesIO as StringIO

try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

import hashlib


class InvalidChecksumException(Exception):
    pass


class Downloader(object):
    @classmethod
    def download(cls, url, checksum=None):
        if url.startswith('http'):
            print("Downloading '%s'" % url)
            return cls.download_http(url, checksum)

    @classmethod
    def download_http(self, url, checksum=None):
        response = urlopen(url).read()

        if checksum is not None:
            cypher, hexdigest = checksum.split('$')
            computed_hexdigest = getattr(hashlib, cypher)(response).hexdigest()
            if computed_hexdigest != hexdigest:
                raise InvalidChecksumException(computed_hexdigest)

        return StringIO(response)
