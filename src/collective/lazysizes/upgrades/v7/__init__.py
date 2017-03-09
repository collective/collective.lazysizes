# -*- coding: utf-8 -*-
from collective.lazysizes.config import IS_PLONE_5
from collective.lazysizes.logger import logger
from plone import api


JS = '++resource++collective.lazysizes/ls.respimg.min.js'


def remove_respimg_polyfill(setup_tool):
    """Remove respimg polyfill plugin."""
    if IS_PLONE_5:
        record = 'plone.bundles/plone-legacy.resources'
        resources = api.portal.get_registry_record(record)
        id_ = 'resource-collective-lazysizes-ls-respimg-min-js'
        if id_ in resources:
            resources.remove(id_)
            api.portal.set_registry_record(record, resources)
            assert id_ not in api.portal.get_registry_record(record)

    # we run this code in Plone 5 also "just in case"
    portal_js = api.portal.get_tool('portal_javascripts')
    if JS in portal_js.getResourceIds():
        portal_js.unregisterResource(JS)
        assert JS not in portal_js.getResourceIds()
        logger.info('respimg polyfill plugin was removed')
