#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

import codecs
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

NAME = 'pyplwnxml'
DESCRIPTION = 'Parser for plwnxml (format of polish wordnet - słowosieć)'
URL = 'https://github.com/red-rocket-dev/pyplwnxml'
EMAIL = 'redrocketdev@gmail.com'
AUTHOR = 'Jakub Płonka'

REQUIRED = [
    'aenum'
]


here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

about = {}
with open(os.path.join(here, NAME, '__version__.py')) as f:
    exec(f.read(), about)


class PublishCommand(Command):
    description = 'Build and publish the package.'
    user_options = []
    
    @staticmethod
    def status(s):
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.sep.join(('.', 'dist')))
        except FileNotFoundError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    install_requires=REQUIRED,
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=['nose'],
    license='ISC',
    classifiers=[
        'License :: OSI Approved :: ISC License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Natural Language :: Polish'
    ],
    cmdclass={
        'publish': PublishCommand,
    },
)
