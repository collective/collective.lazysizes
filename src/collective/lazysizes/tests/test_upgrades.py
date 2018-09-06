# -*- coding: utf-8 -*-
from collective.lazysizes.config import IS_PLONE_5
from collective.lazysizes.testing import INTEGRATION_TESTING
from plone import api

import unittest


class UpgradeTestCaseBase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self, from_version, to_version):
        self.portal = self.layer['portal']
        self.setup = self.portal['portal_setup']
        self.profile_id = u'collective.lazysizes:default'
        self.from_version = from_version
        self.to_version = to_version

    def get_upgrade_step(self, title):
        """Get the named upgrade step."""
        self.setup.setLastVersionForProfile(self.profile_id, self.from_version)
        upgrades = self.setup.listUpgrades(self.profile_id)
        steps = [s for s in upgrades[0] if s['title'] == title]
        return steps[0] if steps else None

    def execute_upgrade_step(self, step):
        """Execute an upgrade step."""
        request = self.layer['request']
        request.form['profile_id'] = self.profile_id
        request.form['upgrades'] = [step['id']]
        self.setup.manage_doUpgrades(request=request)

    @property
    def total_steps(self):
        """Return the number of steps in the upgrade."""
        self.setup.setLastVersionForProfile(self.profile_id, self.from_version)
        upgrades = self.setup.listUpgrades(self.profile_id)
        assert len(upgrades) > 0
        return len(upgrades[0])


class To2TestCase(UpgradeTestCaseBase):

    def setUp(self):
        UpgradeTestCaseBase.setUp(self, u'1', u'2')

    def test_upgrade_to_2_registrations(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertGreaterEqual(int(version), int(self.to_version))
        self.assertEqual(self.total_steps, 2)

    def test_add_new_field_to_configlet(self):
        title = u'Add new field to configlet'
        step = self.get_upgrade_step(title)
        self.assertIsNotNone(step)

        from collective.lazysizes.interfaces import ILazySizesSettings
        from plone.registry.interfaces import IRegistry
        from zope.component import getUtility
        registry = getUtility(IRegistry)

        # simulate state on previous version
        record = ILazySizesSettings.__identifier__ + '.css_class_blacklist'
        del registry.records[record]

        with self.assertRaises(KeyError):
            registry.forInterface(ILazySizesSettings)

        # execute upgrade step and verify changes were applied
        self.execute_upgrade_step(step)

        settings = registry.forInterface(ILazySizesSettings)
        self.assertTrue(hasattr(settings, 'css_class_blacklist'))
        self.assertEqual(settings.css_class_blacklist, set([]))


class To3TestCase(UpgradeTestCaseBase):

    def setUp(self):
        UpgradeTestCaseBase.setUp(self, u'2', u'3')

    def test_upgrade_to_2_registrations(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertGreaterEqual(int(version), int(self.to_version))
        self.assertEqual(self.total_steps, 1)


class To4TestCase(UpgradeTestCaseBase):

    def setUp(self):
        UpgradeTestCaseBase.setUp(self, u'3', u'4')

    def test_upgrade_to_2_registrations(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertGreaterEqual(int(version), int(self.to_version))
        self.assertEqual(self.total_steps, 2)


class To5TestCase(UpgradeTestCaseBase):

    def setUp(self):
        UpgradeTestCaseBase.setUp(self, u'4', u'5')

    def test_upgrade_to_2_registrations(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertGreaterEqual(int(version), int(self.to_version))
        self.assertEqual(self.total_steps, 2)

    @unittest.skipIf(IS_PLONE_5, 'Upgrade step not supported under Plone 5')
    def test_use_amd_version(self):
        # check if the upgrade step is registered
        title = u'Use AMD version of Lazysizes'
        step = self.get_upgrade_step(title)
        assert step is not None

        # simulate state on previous version
        from collective.lazysizes.upgrades.v5 import NEW_JS
        from collective.lazysizes.upgrades.v5 import OLD_JS
        portal_js = api.portal.get_tool('portal_javascripts')
        portal_js.registerResource(OLD_JS)
        assert OLD_JS in portal_js.getResourceIds()

        # run the upgrade step to validate the update
        self.execute_upgrade_step(step)
        self.assertNotIn(OLD_JS, portal_js.getResourceIds())
        self.assertIn(NEW_JS, portal_js.getResourceIds())


class To6TestCase(UpgradeTestCaseBase):

    def setUp(self):
        UpgradeTestCaseBase.setUp(self, u'5', u'6')

    def test_upgrade_to_6_registrations(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertGreaterEqual(int(version), int(self.to_version))
        self.assertEqual(self.total_steps, 1)


class To7TestCase(UpgradeTestCaseBase):

    def setUp(self):
        UpgradeTestCaseBase.setUp(self, u'6', u'7')

    def test_registrations(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertGreaterEqual(int(version), int(self.to_version))
        self.assertEqual(self.total_steps, 2)

    @unittest.skipIf(IS_PLONE_5, 'Upgrade step not supported under Plone 5')
    def test_remove_respimg_polyfill(self):
        # check if the upgrade step is registered
        title = u'Remove respimg polyfill plugin'
        step = self.get_upgrade_step(title)
        assert step is not None

        # simulate state on previous version
        from collective.lazysizes.upgrades.v7 import JS
        portal_js = api.portal.get_tool('portal_javascripts')
        portal_js.registerResource(JS)
        assert JS in portal_js.getResourceIds()

        # run the upgrade step to validate the update
        self.execute_upgrade_step(step)
        self.assertNotIn(JS, portal_js.getResourceIds())


class To8TestCase(UpgradeTestCaseBase):

    def setUp(self):
        UpgradeTestCaseBase.setUp(self, u'7', u'8')

    def test_registrations(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertGreaterEqual(int(version), int(self.to_version))
        self.assertEqual(self.total_steps, 1)

    def test_add_new_field_to_configlet(self):
        title = u'Add lazyload_authenticated field to configlet'
        step = self.get_upgrade_step(title)
        self.assertIsNotNone(step)

        from collective.lazysizes.interfaces import ILazySizesSettings
        from plone.registry.interfaces import IRegistry
        from zope.component import getUtility
        registry = getUtility(IRegistry)

        # simulate state on previous version
        record = ILazySizesSettings.__identifier__ + '.lazyload_authenticated'
        del registry.records[record]

        with self.assertRaises(KeyError):
            registry.forInterface(ILazySizesSettings)

        # execute upgrade step and verify changes were applied
        self.execute_upgrade_step(step)

        settings = registry.forInterface(ILazySizesSettings)
        self.assertTrue(hasattr(settings, 'lazyload_authenticated'))
        self.assertEqual(settings.lazyload_authenticated, False)


class To9TestCase(UpgradeTestCaseBase):

    def setUp(self):
        UpgradeTestCaseBase.setUp(self, u'8', u'9')

    def test_registrations(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertGreaterEqual(int(version), int(self.to_version))
        self.assertEqual(self.total_steps, 1)


class To10TestCase(UpgradeTestCaseBase):

    def setUp(self):
        UpgradeTestCaseBase.setUp(self, u'9', u'10')

    def test_registrations(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertGreaterEqual(int(version), int(self.to_version))
        self.assertEqual(self.total_steps, 2)

    @unittest.skipIf(IS_PLONE_5, 'Plone 4.3')
    def test_deprecate_resource_registries_plone_4(self):
        # check if the upgrade step is registered
        title = u'Deprecate resource registries'
        step = self.get_upgrade_step(title)
        self.assertIsNotNone(step)

        # simulate state on previous version
        RESOURCES = set([
            '++resource++collective.lazysizes/ls.twitter.min.js',
            '++resource++collective.lazysizes/lazysizes-umd.min.js',
        ])
        jsregistry = api.portal.get_tool('portal_javascripts')
        for id_ in RESOURCES:
            jsregistry.registerResource(id_)

        # the intersection is not an empty set (elements in common)
        self.assertTrue(set(jsregistry.getResourceIds()) & RESOURCES)

        # run the upgrade step to validate the update
        self.execute_upgrade_step(step)

        # the intersection is an empty set (no elements in common)
        self.assertFalse(set(jsregistry.getResourceIds()) & RESOURCES)
