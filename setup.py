#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
doclink = """
Documentation
-------------

The full documentation is at http://feedbackbot.rtfd.org."""
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='feedbackbot',
    version='0.0.1',
    description='Slack bot to provide teammates with anonymous feedback.',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='Matt Davidson',
    author_email='matthewdavidson12@gmail.com',
    url='https://github.com/mattjdavidson/feedbackbot',
    packages=[
        'feedbackbot',
    ],
    package_dir={'feedbackbot': 'feedbackbot'},
    include_package_data=True,
    install_requires=[
    ],
    license='MIT',
    zip_safe=False,
    keywords='feedbackbot',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)
