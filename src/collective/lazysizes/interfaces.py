# -*- coding: utf-8 -*-
from collective.lazysizes import _
from plone.directives import form
from zope import schema
from zope.interface import Interface


class ILazySizesLayer(Interface):

    """A layer specific for this add-on product."""


class ILazySizesSettings(form.Schema):

    """Schema for the control panel form."""

    image_candidates = schema.List(
        title=_(u'Image candidates'),
        description=_(
            u'A list of image scales to be used as image candidate strings.'),
        required=True,
        default=[],
        value_type=schema.Choice(
            vocabulary=u'collective.lazysizes.ImageScales'),
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
