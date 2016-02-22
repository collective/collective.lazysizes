# -*- coding:utf-8 -*-
from collective.lazysizes.config import PROJECTNAME
from plone import api

import logging


logger = logging.getLogger(PROJECTNAME)


def cook_javascript_resources(context):
    """Cook JavaScripts resources."""
    js_tool = api.portal.get_tool('portal_javascripts')
    js_tool.cookResources()
    logger.info('JavaScripts resources were cooked')
