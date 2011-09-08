"""Veliberator module"""
import os
import gettext

__version__ = '0.3.dev'
__license__ = 'BSD License'

__author__ = 'Fantomas42'
__email__ = 'fantomas42@gmail.com'

__url__ = 'http://veliberator.com/'

gettext.install('veliberator', os.path.join(os.path.dirname(__file__),
                                            'locale'), unicode=1)
