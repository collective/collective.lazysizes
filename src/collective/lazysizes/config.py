# -*- coding: utf-8 -*-
from plone import api


PROJECTNAME = 'collective.lazysizes'

IS_PLONE_5 = api.env.plone_version().startswith('5')
