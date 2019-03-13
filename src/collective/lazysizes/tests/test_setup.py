# -*- coding: utf-8 -*-
from collective.lazysizes.config import PROJECTNAME
from collective.lazysizes.interfaces import ILazySizesLayer
from collective.lazysizes.testing import INTEGRATION_TESTING
from collective.lazysizes.testing import IS_BBB
from collective.lazysizes.testing import QIBBB
from plone.browserlayer.utils import registered_layers

import unittest


JS = (
    '++resource++collective.lazysizes/lazysizes.js',
)


class InstallTestCase(unittest.TestCase):

    """Ensure product is properly installed."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    @unittest.skipIf(IS_BBB, 'Plone >= 5.1')
    def test_installed(self):
        from Products.CMFPlone.utils import get_installer
        qi = get_installer(self.portal, self.request)
        self.assertTrue(qi.is_product_installed(PROJECTNAME))

    @unittest.skipUnless(IS_BBB, 'Plone < 5.1')
    def test_installed_BBB(self):
        qi = self.portal['portal_quickinstaller']
        self.assertTrue(qi.isProductInstalled(PROJECTNAME))

    def test_addon_layer(self):
        self.assertIn(ILazySizesLayer, registered_layers())

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
            setup_tool.getLastVersionForProfile(profile), (u'10',))


class UninstallTestCase(unittest.TestCase, QIBBB):
    """Ensure product is properly uninstalled."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.qi = self.uninstall()  # BBB: QI compatibility

    @unittest.skipIf(IS_BBB, 'Plone >= 5.1')
    def test_uninstalled(self):
        self.assertFalse(self.qi.is_product_installed(PROJECTNAME))

    @unittest.skipUnless(IS_BBB, 'Plone < 5.1')
    def test_uninstalled_BBB(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_addon_layer_removed(self):
        self.assertNotIn(ILazySizesLayer, registered_layers())
