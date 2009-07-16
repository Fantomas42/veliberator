from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='veliberator',
      version=version,
      description="Python API for Velib.",
      long_description="""Veliberator provides an API for getting informations
about the stations of the Velib city network""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='api, velib, service',
      author='Fantomas42',
      author_email='fantomas42@gmail.com',
      url='http://veliberator.com',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
