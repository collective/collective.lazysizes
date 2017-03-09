# -*- coding: utf-8 -*-
from collective.lazysizes.config import IS_PLONE_5
from collective.lazysizes.config import PROJECTNAME
from collective.lazysizes.interfaces import ILazySizesLayer
from collective.lazysizes.testing import INTEGRATION_TESTING
from plone import api
from plone.browserlayer.utils import registered_layers

import unittest


JS = (
    '++resource++collective.lazysizes/ls.twitter.min.js',
    '++resource++collective.lazysizes/lazysizes-umd.min.js',
)


class InstallTestCase(unittest.TestCase):

    """Ensure product is properly installed."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_installed(self):
        qi = self.portal['portal_quickinstaller']
        self.assertTrue(qi.isProductInstalled(PROJECTNAME))

    def test_addon_layer(self):
        self.assertIn(ILazySizesLayer, registered_layers())

    @unittest.skipIf(IS_PLONE_5, 'No easy way to test this under Plone 5')
    def test_jsregistry(self):
        resource_ids = self.portal['portal_javascripts'].getResourceIds()
        for js in JS:
            self.assertIn(js, resource_ids, '{0} not installed'.format(js))

    def test_setup_permission(self):
        permission = 'collective.lazysizes: Setup'
        roles = self.portal.rolesOfPermission(permission)
        roles = [r['name'] for r in roles if r['selected']]
        expected = ['Manager', 'Site Administrator']
        self.assertListEqual(roles, expected)

    def test_version(self):
        profile = 'collective.lazysizes:default'
        setup_tool = self.portal['portal_setup']
        self.assertEqual(
            setup_tool.getLastVersionForProfile(profile), (u'7',))


class UninstallTestCase(unittest.TestCase):

    """Ensure product is properly uninstalled."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']

        with api.env.adopt_roles(['Manager']):
            self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_addon_layer_removed(self):
        self.assertNotIn(ILazySizesLayer, registered_layers())

    @unittest.skipIf(IS_PLONE_5, 'No easy way to test this under Plone 5')
    def test_jsregistry_removed(self):
        resource_ids = self.portal['portal_javascripts'].getResourceIds()
        for js in JS:
            self.assertNotIn(js, resource_ids, '{0} not installed'.format(js))
