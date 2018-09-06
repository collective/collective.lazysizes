# -*- coding: utf-8 -*-
from collective.lazysizes.config import JS
from plone.app.layout.viewlets import ViewletBase


class ResourcesViewlet(ViewletBase):
    """This viewlet inserts static resources on page header."""

    def js(self):
        return self.site_url + '/' + JS
