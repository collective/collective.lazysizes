# -*- coding: utf-8 -*-
from collective.lazysizes.config import IS_PLONE_5


# BBB: avoid ImportError while running upgrade step
#      with plone.app.registry <1.5
if not IS_PLONE_5:
    import Products.CMFPlone.interfaces
    Products.CMFPlone.interfaces.IBundleRegistry = {}
    Products.CMFPlone.interfaces.IResourceRegistry = {}
