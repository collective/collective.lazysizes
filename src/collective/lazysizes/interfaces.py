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
