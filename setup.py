import os
import sys
from setuptools import setup, find_packages


def read(fname):
    try:
        with open(os.path.join(os.path.dirname(__file__), fname)) as fh:
            return fh.read()
    except IOError:
        return ''


requirements = read('REQUIREMENTS').splitlines()
tests_requirements = read('TEST-REQUIREMENTS').splitlines()

packages = find_packages(exclude=['tests'])

# Avoid byte-compiling the shipped template
sys.dont_write_bytecode = True

setup(
    name="cookiejar",
    version="0.0.1",
    description="Cookiecutter templates discovery and management.",
    long_description=read('README.rst'),
    url='https://github.com/fcurella/cookiejar',
    license='MIT',
    author='Flavio Curella',
    author_email='flavio.curella@gmail.com',
    packages=packages,
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    scripts=['bin/cookiejar'],
    install_requires=requirements,
    tests_require=tests_requirements,
)
