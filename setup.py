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

    description="Veliberator provides a Python API for getting informations "
    "about the stations of the Velib' network.",
    long_description=open(os.path.join('README.rst')).read(),
    keywords='velib, api, service',

    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ],

    entry_points={
        'console_scripts': [
            'veliberator=veliberator.scripts.command_line:cmdline',
            ]
    },
    test_suite='veliberator.tests.global_test_suite',
    packages=find_packages(exclude=['tests']),

    zip_safe=False,
    platforms='any',
    include_package_data=True,

    install_requires=['SQLAlchemy==0.7.10',
                      'Elixir==0.7.1',
                      'simplejson'],
)
