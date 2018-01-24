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
        title=_(
            'title_lazyload_authenticated',
            default=u'Enable for authenticated users?',
        ),
        description=_(
            'description_lazyload_authenticated',
            default=u''
            u'By default, images and iframes are lazy loaded only for '
            u'anonymous users. If selected, lazy loading will be enabled for '
            u'all users.',
        ),
        default=False,
    )

    form.widget('css_class_blacklist', cols=25, rows=10)
    css_class_blacklist = schema.Set(
        title=_(
            'title_css_class_blacklist',
            default=u'CSS class blacklist',
        ),
        description=_(
            'description_css_class_blacklist',
            default=u''
            u'A list of CSS class identifiers that will not be processed for '
            u'lazy loading. &lt;img&gt; and &lt;iframe&gt; elements with that '
            u'class directly applied to them, or to a parent element, will be '
            u'skipped.',
        ),
        required=False,
        default=set(),
        value_type=schema.ASCIILine(title=_(
            'title_css_class_blacklist_value_type',
            default=u'CSS class',
        )),
    )
