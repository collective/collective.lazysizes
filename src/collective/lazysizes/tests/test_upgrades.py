# -*- coding: utf-8 -*-
from collective.lazysizes.testing import INTEGRATION_TESTING

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
        self.assertTrue(version >= self.to_version)
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
        self.assertTrue(version >= self.to_version)
        self.assertEqual(self.total_steps, 1)
