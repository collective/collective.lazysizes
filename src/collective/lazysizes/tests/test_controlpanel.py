# -*- coding: utf-8 -*-
from collective.lazysizes.interfaces import ILazySizesSettings
from collective.lazysizes.testing import INTEGRATION_TESTING
from collective.lazysizes.testing import QIBBB
from plone.app.testing import logout
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import unittest


class ControlPanelTestCase(unittest.TestCase, QIBBB):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.controlpanel = self.portal['portal_controlpanel']

    def test_controlpanel_view_is_protected(self):
        from AccessControl import Unauthorized
        logout()
        with self.assertRaises(Unauthorized):
            self.portal.restrictedTraverse('@@lazysizes-settings')

    def test_controlpanel_installed(self):
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertIn('lazysizes', actions)

    def test_controlpanel_removed_on_uninstall(self):
        self.uninstall()  # BBB: QI compatibility

        actions = [
            a.getAction(self)['id'] for a in self.controlpanel.listActions()]
        self.assertNotIn('lazysizes', actions)


class RegistryTestCase(unittest.TestCase, QIBBB):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(ILazySizesSettings)

    def test_lazyload_authenticated_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'lazyload_authenticated'))
        self.assertEqual(self.settings.lazyload_authenticated, False)

    def test_css_class_blacklist_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'css_class_blacklist'))
        self.assertEqual(self.settings.css_class_blacklist, set([]))

    def test_records_removed_on_uninstall(self):
        self.uninstall()  # BBB: QI compatibility

        records = [
            ILazySizesSettings.__identifier__ + '.lazyload_authenticated',
            ILazySizesSettings.__identifier__ + '.css_class_blacklist',
        ]

        for r in records:
            self.assertNotIn(r, self.registry)
