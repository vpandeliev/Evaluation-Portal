#!/usr/bin/env python
#comment ADDED! testing forking etc.
from distutils.core import setup

setup(
    name='portal',
    version='1.0',
    description='Evaluation portal',
    author='Velian Pandeliev',
    packages=['portal', 'portal.studies', 'portal.assess','portal.boggle','portal.rushhour'],
    )
