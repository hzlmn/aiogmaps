import io
import os
import re
import sys

from setuptools import setup


def get_version():
    regex = r"__version__\s=\s\'(?P<version>[\d\.]+?)\'"

    path = ('aiogmaps', '__init__.py',)

    return re.search(regex, read(*path)).group('version')


def read(*parts):
    filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), *parts)

    sys.stdout.write(filename)

    with io.open(filename, encoding='utf-8', mode='rt') as fp:
        return fp.read()


packages = ['aiogmaps']


install_requires = ['aiohttp>=2.3.5', 'googlemaps']


classifiers = ['Intended Audience :: Developers',
               'License :: OSI Approved :: MIT License',
               'Programming Language :: Python',
               'Programming Language :: Python :: 3.6',
               ]

setup(
    name='aiogmaps',
    version=get_version(),
    description='Asyncio client library for Google Maps API Web Services',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/hzlmn/aiogmaps',
    author='Oleh Kuchuk',
    author_email='kuchuklehjs@gmail.com',
    license='MIT',
    packages=packages,
    install_requires=install_requires,
    zip_safe=False,
    classifiers=classifiers,
    keywords=[
        'asyncio',
        'aiohttp',
    ],
)
