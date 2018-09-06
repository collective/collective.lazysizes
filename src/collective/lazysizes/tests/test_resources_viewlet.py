# -*- coding: utf-8 -*-
from collective.lazysizes.testing import INTEGRATION_TESTING
from lxml import etree  # nosec
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter
from zope.viewlet.interfaces import IViewletManager

import unittest


class ResourcesViewletTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        self.viewlet = self.get_viewlet(self.portal)

    def get_viewlet_manager(self, context, name='plone.htmlhead'):
        request = self.request
        view = BrowserView(context, request)
        manager = getMultiAdapter(
            (context, request, view), IViewletManager, name)
        return manager

    def get_viewlet(self, context, name='collective.lazysizes.resources'):
        manager = self.get_viewlet_manager(context)
        manager.update()
        viewlet = [v for v in manager.viewlets if v.__name__ == name]
        assert len(viewlet) == 1  # nosec
        return viewlet[0]

    def test_viewlet(self):
        html = etree.HTML(self.viewlet())
        self.assertIn('async', html.xpath('//script')[0].attrib)
        # script name must include the hash of latest git commit
        regexp = r'lazysizes-[\da-f]{7}\.js$'
        self.assertRegexpMatches(
            html.xpath('//script')[0].attrib['src'], regexp)
