# -*- coding: utf-8 -*-
from collective.lazysizes.config import IS_PLONE_5
from collective.lazysizes.logger import logger
from plone import api


NEW_JS = '++resource++collective.lazysizes/lazysizes-umd.min.js'
OLD_JS = '++resource++collective.lazysizes/lazysizes.min.js'


def use_amd_version(setup_tool):
    """Use AMD version of Lazysizes."""
    if IS_PLONE_5:
        logger.warn('Upgrade step not supported under Plone 5')
        return

    portal_js = api.portal.get_tool('portal_javascripts')
    if OLD_JS in portal_js.getResourceIds():
        portal_js.renameResource(OLD_JS, NEW_JS)
        assert NEW_JS in portal_js.getResourceIds()
        logger.info('lazysizes was upgraded; using now the AMD module')
