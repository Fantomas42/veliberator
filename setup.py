"""Setup script for veliberator"""
import os

from setuptools import setup
from setuptools import find_packages

import veliberator

setup(
    name='veliberator',
    version=veliberator.__version__,
    license=veliberator.__license__,

    author=veliberator.__author__,
    author_email=veliberator.__email__,
    url=veliberator.__url__,

    description='Python API for Velib.',
    long_description=open(os.path.join('README.rst')).read(),
    keywords='velib, api, service',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ],

    scripts=['./veliberator/scripts/find_place.py',
             './veliberator/scripts/synchronize.py'],
    data_files=[('/etc', ['etc/veliberator.cfg']),],
    test_suite = 'tests.global_test_suite',
    packages=find_packages(exclude=['tests',]),

    zip_safe=False,
    platforms = 'any',
    include_package_data=True,

    install_requires = ['SQLAlchemy>=0.5',
                        'Elixir>=0.7.0',
                        'simplejson>=2.0.9'],
    )
