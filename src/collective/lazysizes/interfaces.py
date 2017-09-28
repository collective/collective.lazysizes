# -*- coding: utf-8 -*-
from collective.lazysizes import _
from plone.autoform import directives as form
from plone.supermodel import model
from zope import schema
from zope.interface import Interface


class ILazySizesLayer(Interface):

    """A layer specific for this add-on product."""


class ILazySizesSettings(model.Schema):
    """Schema for the control panel form."""

    lazyload_authenticated = schema.Bool(
        title=_(u'Enable for authenticated users?'),
        description=_(
            u'By default, images and iframes are lazy loaded only for anonymous users. '
            u'If selected, lazy loading will be enabled for all users.'
        ),
        default=False,
    )

    form.widget('css_class_blacklist', cols=25, rows=10)
    css_class_blacklist = schema.Set(
        title=_(u'CSS class blacklist'),
        description=_(
            u'A list of CSS class identifiers that will not be processed for lazy loading. '
            u'&lt;img&gt; and &lt;iframe&gt; elements with that class directly applied to them, or to a parent element, will be skipped.'
        ),
        required=False,
        default=set([]),
        value_type=schema.ASCIILine(title=_(u'CSS class')),
    )
