"""Installing veliberator"""
from setuptools import setup, find_packages
import sys, os

from veliberator import VERSION

setup(
    name='veliberator',
    version=VERSION,
    zip_safe=True,

    scripts=['./bin/find_place.py',
             './bin/synchronize.py'],
    data_files=[('/etc', ['etc/veliberator.cfg']),],

    packages=find_packages(exclude=['tests',]),
    install_requires = ['SQLAlchemy>=0.5',
                        'Elixir>=0.7.0',
                        'simplejson>=2.0.9'],
    include_package_data=True,
        
    test_suite = 'tests.global_test_suite',

    author='Fantomas42',
    author_email='fantomas42@gmail.com',
    url='http://veliberator.com',
 
    license='GPL',
    platforms = 'any',
    description='Python API for Velib.',
    long_description=open(os.path.join('docs', 'README.txt')).read(),
    keywords='velib, api, service',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    )
