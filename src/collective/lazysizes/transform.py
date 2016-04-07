# -*- coding: utf-8 -*-
from collective.lazysizes.interfaces import ILazySizesSettings
from collective.lazysizes.logger import logger
from lxml import etree
from plone import api
from plone.transformchain.interfaces import ITransform
from repoze.xmliter.utils import getHTMLSerializer
from zope.interface import implementer


# grey rectangule, 16x16
PLACEHOLDER = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQAQMAAAAlPW0iAAAAA1BMVEXy8vJkA4prAAAAC0lEQVQI12MgEQAAADAAAWV61nwAAAAASUVORK5CYII='

# to avoid additional network round trips to render content above the fold
# we only process elements inside the "content" element
ROOT_SELECTOR = '//*[@id="content"]'

# elements by CSS class; http://stackoverflow.com/a/1604480
CLASS_SELECTOR = '//*[contains(concat(" ", normalize-space(@class), " "), " {0} ")]'


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
            return  # this should never happen

        try:
            element.attrib['data-src'] = element.attrib['src']
        except KeyError:
            url = self.request['URL']
            logger.error('<img> tag without src attribute in: ' + url)
            return

        classes.append('lazyload')
        element.attrib['class'] = ' '.join(classes).strip()

        if element.tag == 'img':
            element.attrib['src'] = PLACEHOLDER
        elif element.tag == 'iframe':
            del element.attrib['src']

        msg = '<{0}> with src="{1}" was processed for lazy loading.'
        logger.debug(msg.format(element.tag, element.attrib['data-src']))

    def _blacklist(self, result, blacklisted_classes):
        """Return a list of blacklisted elements."""
        if not blacklisted_classes:
            return ()

        path = []
        for css_class in blacklisted_classes:
            path.append('{0}{1}//img|{0}{1}//iframe'.format(
                ROOT_SELECTOR, CLASS_SELECTOR.format(css_class)))

        path = '|'.join(path)
        return result.tree.xpath(path)

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

        record = ILazySizesSettings.__identifier__ + '.css_class_blacklist'
        blacklist = api.portal.get_registry_record(record)
        blacklist = self._blacklist(result, blacklist)

        path = '{0}//img|{0}//iframe'.format(ROOT_SELECTOR)
        for el in result.tree.xpath(path):
            if el in blacklist:
                continue
            self._lazyload(el)

        return result
