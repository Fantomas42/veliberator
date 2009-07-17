"""Installing veliberator"""
from setuptools import setup, find_packages
import sys, os

version = '0.1.2'

setup(
    name='veliberator',
    version=version,
    zip_safe=True,

    scripts=['./bin/find_place.py',
             './bin/synchronize.py'],
    packages=find_packages(exclude=['tests',]),
    install_requires = ['SQLAlchemy>=0.5',
                        'Elixir>=0.6.1',],
    include_package_data=True,
        
    test_suite = 'tests.global_test_suite',

    author='Fantomas42',
    author_email='fantomas42@gmail.com',
    url='http://fantomas.willbreak.it',
 
    license='GPL',
    platforms = 'any',
    description="Python API for Velib.",
    long_description=open(os.path.join("docs", "README.txt")).read(),
    keywords='velib, api, service',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    )
