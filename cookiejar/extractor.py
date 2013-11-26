from fnmatch import fnmatch
import os
import shutil
from tarfile import TarFile
from zipfile import ZipFile

from .downloader import Downloader


# Standard Library is not very standard.
class ArchiveFileWrapper(object):
    blacklist = ('.DS_Store', "*.pyc", "__MACOSX/*")

    def __init__(self, template_name):
        self.template_name = template_name

    def is_blacklisted(self, member_name):
        for blacklisted in self.blacklist:
            if fnmatch(member_name, blacklisted):
                return True
        return False

    def extract_members(self, destination):
        pardir = os.path.pardir + os.path.sep
        curdir = os.path.curdir + os.path.sep

        members = self.names()
        for member in members:
            if self.is_blacklisted(member):
                continue

            if member.startswith(curdir) or member.startswith(pardir) or member.startswith(os.path.sep):
                raise RuntimeError("Archive is unsafe.")

            try:
                outfile = os.path.sep.join([self.template_name] + member.split(os.path.sep)[1:])
            except IndexError:
                continue

            outpath = os.path.join(destination, outfile)

            if not outpath.endswith(os.path.sep):
                parent_dir = os.path.dirname(outpath)
                if not os.path.exists(parent_dir):
                    os.makedirs(parent_dir)
                with open(outpath, 'wb') as fh:
                    fh.write(self.extract_file(member).read())

    def names(self):
        raise NotImplemented


class ZipFileWrapper(ArchiveFileWrapper):
    def __init__(self, fh, *args, **kwargs):
        self.archive = ZipFile(fh)
        super(ZipFileWrapper, self).__init__(*args, **kwargs)

    def extract_file(self, *args, **kwargs):
        return self.archive.open(*args, **kwargs)

    def names(self):
        return self.archive.namelist()


class TarFileWrapper(ArchiveFileWrapper):
    def __init__(self, fh, *args, **kwargs):
        self.archive = TarFile(fileobj=fh)
        super(TarFileWrapper, self).__init__(*args, **kwargs)

    def extract_file(self, *args, **kwarg):
        return self.archive.extractfile(*args, **kwarg)

    def names(self):
        return self.archive.getnames()


class PackageExtractor(object):
    extract_dir = None

    def __init__(self, settings, url, template_name):
        self.settings = settings
        self.template_name = template_name
        self.url = url
        super(PackageExtractor, self).__init__()

    def download(self, url, checksum=None):
        response = Downloader.download(url, checksum)

        if url.endswith('.zip'):
            self.archive = ZipFileWrapper(response, self.template_name)
        elif url.endswith('.tgz'):
            self.archive = TarFileWrapper(response, self.template_name)
        elif url.endswith('.tar.gz'):
            self.archive = TarFileWrapper(response, self.template_name)

        return self

    def extract(self, archive=None):
        destination = self.settings['templates_dir']
        if archive is None:
            archive = self.archive
        archive.extract_members(destination)

        self.extract_dir = destination

    def cleanup(self):
        if self.extract_dir is not None:
            shutil.rmtree(self.extract_dir)

