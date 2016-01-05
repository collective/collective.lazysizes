# -*- coding: utf-8 -*-
from collective.lazysizes.logger import logger
from lxml import etree
from plone import api
from plone.transformchain.interfaces import ITransform
from repoze.xmliter.utils import getHTMLSerializer
from zope.interface import implementer


@implementer(ITransform)
class LazySizesTransform(object):

    """Transform a response to lazy load <img> and <iframe> elements."""

    order = 8888

    def __init__(self, published, request):
        self.published = published
        self.request = request

    def _parse(self, result):
        """Create an XMLSerializer from an HTML string, if needed."""
        content_type = self.request.response.getHeader('Content-Type')
        if not content_type or not content_type.startswith('text/html'):
            return None

        try:
            return getHTMLSerializer(result)
        except (AttributeError, TypeError, etree.ParseError):
            return None

    def _lazyload(self, element):
        """Inject attributes needed by lazysizes to lazy load elements:

        * add the "lazyload" class
        * add a data-src attribute with the referenced object
        * if the element is an img, set the src attribute with a low
          resolution scale of the image

        For more information, see: https://afarkas.github.io/lazysizes/
        """
        classes = element.attrib.get('class', '').split(' ')
        if 'lazyload' in classes:
            return  # already processed (I don't know if this could happen)

        classes.append('lazyload')
        element.attrib['class'] = ' '.join(classes).strip()
        element.attrib['data-src'] = element.attrib['src']

        if element.tag == 'img':
            portal_url = api.portal.get().absolute_url()
            element.attrib['src'] = portal_url + '/spinner.gif'
        elif element.tag == 'iframe':
            del element.attrib['src']

        msg = '<{0}> with src="{1}" was processed for lazy loading.'
        logger.info(msg.format(element.tag, element.attrib['data-src']))

    def transformBytes(self, result, encoding):
        return None

    def transformUnicode(self, result, encoding):
        return None

    def transformIterable(self, result, encoding):
        if not api.user.is_anonymous():
            return None

        result = self._parse(result)
        if result is None:
            return None

        # we only process elements inside the "content" <div>
        root = '//div[@id="content"]'
        [self._lazyload(e) for e in result.tree.xpath(root + '//img')]
        [self._lazyload(e) for e in result.tree.xpath(root + '//iframe')]

        return result
