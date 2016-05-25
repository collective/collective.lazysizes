# -*- coding:utf-8 -*-
from collective.lazysizes.logger import logger
from plone import api


def cook_javascript_resources(context):  # pragma: no cover
    """Cook JavaScripts resources."""
    js_tool = api.portal.get_tool('portal_javascripts')
    js_tool.cookResources()
    logger.info('JavaScripts resources were cooked')
