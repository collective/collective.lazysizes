# -*- coding: utf-8 -*-
from collective.lazysizes.config import IS_PLONE_5
from collective.lazysizes.logger import logger
from plone import api


NEW_JS = '++resource++collective.lazysizes/lazysizes.js'
OLD_JS = '++resource++collective.lazysizes/lazysizes-umd.min.js'
TWITTER_JS = '++resource++collective.lazysizes/ls.twitter.min.js'


def update_static_resources(setup_tool):
    """Use resource compiled from webpack."""
    if IS_PLONE_5:
        logger.warn('Upgrade step not supported under Plone 5')
        return

    portal_js = api.portal.get_tool('portal_javascripts')
    resource_ids = portal_js.getResourceIds()
    if OLD_JS in resource_ids:
        portal_js.renameResource(OLD_JS, NEW_JS)
        logger.info('lazysizes was upgraded; using now webpack version')

    assert OLD_JS not in portal_js.getResourceIds()
    assert NEW_JS in portal_js.getResourceIds()

    if TWITTER_JS in portal_js.getResourceIds():
        portal_js.unregisterResource(TWITTER_JS)
        assert TWITTER_JS not in portal_js.getResourceIds()
        logger.info('twitter plugin was removed')
