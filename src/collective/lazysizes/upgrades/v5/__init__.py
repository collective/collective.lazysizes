# -*- coding: utf-8 -*-
from collective.lazysizes.config import IS_PLONE_5
from collective.lazysizes.logger import logger
from plone import api


NEW_JS = '++resource++collective.lazysizes/lazysizes.js'
OLD_JS = '++resource++collective.lazysizes/lazysizes.min.js'


def use_amd_version(setup_tool):
    """Use AMD version of Lazysizes."""
    if IS_PLONE_5:
        logger.warn('Upgrade step not supported under Plone 5')
        return

    portal_js = api.portal.get_tool('portal_javascripts')
    resource_ids = portal_js.getResourceIds()
    if OLD_JS in resource_ids:
        # XXX: https://github.com/collective/collective.lazysizes/issues/46
        if NEW_JS not in resource_ids:
            # profile version 4: not registered, rename the script
            portal_js.renameResource(OLD_JS, NEW_JS)
        else:
            # earlier version: already registered, remove the old script
            portal_js.unregisterResource(OLD_JS)
        logger.info('lazysizes was upgraded; using now the AMD module')

    assert OLD_JS not in portal_js.getResourceIds()  # nosec
    assert NEW_JS in portal_js.getResourceIds()  # nosec
