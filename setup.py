# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

version = '4.1.6'
description = 'Integration of lazysizes, a lightweight lazy loader, into Plone.'
long_description = (
    open('README.rst').read() + '\n' +
    open('CONTRIBUTORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

setup(
    name='collective.lazysizes',
    version=version,
    description=description,
    long_description=long_description,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
        'Framework :: Plone :: 5.1',
        'Framework :: Plone :: 5.2',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='',
    author='Hector Velarde',
    author_email='hector.velarde@gmail.com',
    url='https://github.com/collective/collective.lazysizes',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['collective'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'lxml',
        'plone.api',
        'plone.app.layout',
        'plone.app.registry',
        'plone.autoform',
        'plone.registry',
        'plone.supermodel',
        'plone.transformchain',
        'Products.CMFPlone >=4.3',
        'Products.GenericSetup',
        'repoze.xmliter',
        'setuptools',
        'zope.component',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.schema',
    ],
    extras_require={
        'test': [
            'AccessControl',
            'plone.app.robotframework',
            'plone.app.testing [robot]',
            'plone.browserlayer',
            'plone.registry',
            'plone.testing',
            'robotsuite',
            'testfixtures',
            'zope.viewlet',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
