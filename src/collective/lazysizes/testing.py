# -*- coding: utf-8 -*-
"""Setup testing fixture.

For Plone 5 we need to install plone.app.contenttypes.
"""
from collective.lazysizes.config import PROJECTNAME
from plone import api
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import pkg_resources


try:
    pkg_resources.get_distribution('plone.app.contenttypes')
except pkg_resources.DistributionNotFound:
    from plone.app.testing import PLONE_FIXTURE
else:
    from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE as PLONE_FIXTURE

IS_BBB = api.env.plone_version().startswith('4.3')


class QIBBB:
    """BBB: remove on deprecation of Plone 4.3."""

    def uninstall(self):
        if IS_BBB:
            qi = self.portal['portal_quickinstaller']
            with api.env.adopt_roles(['Manager']):
                qi.uninstallProducts([PROJECTNAME])
        else:
            from Products.CMFPlone.utils import get_installer
            qi = get_installer(self.portal, self.request)
            with api.env.adopt_roles(['Manager']):
                qi.uninstall_product(PROJECTNAME)
        return qi


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.lazysizes
        self.loadZCML(package=collective.lazysizes)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'collective.lazysizes:default')
        portal.portal_workflow.setDefaultChain('one_state_workflow')


FIXTURE = Fixture()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name='collective.lazysizes:Integration')

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name='collective.lazysizes:Functional')

ROBOT_TESTING = FunctionalTesting(
    bases=(FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE, z2.ZSERVER_FIXTURE),
    name='collective.lazysizes:Robot',
)
