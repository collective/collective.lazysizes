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
            return

        try:
            return getHTMLSerializer(result)
        except (AttributeError, TypeError, etree.ParseError):
            return

    def _lazyload_img(self, element):
        """Process <img> tags for lazy loading by using the `src`
        attribute as `data-src` and loading a placeholder instead.

        :param element: the HTML node to be processed
        :type element: instance of lxml.html.HtmlElement
        :returns: the URL of the image to be lazy loaded
        :rtype: str
        """
        assert element.tag == 'img'
        if 'src' not in element.attrib:
            # `src` attribute is mandatory for <img> tags
            url = self.request['URL']
            logger.error('<img> tag without src attribute in: ' + url)
            return
        element.attrib['data-src'] = element.attrib['src']
        element.attrib['src'] = PLACEHOLDER
        return element.attrib['data-src']

    def _lazyload_iframe(self, element):
        """Process <iframe> tags for lazy loading by replacing the
        `src` attribute with a `data-src`.

        :param element: the HTML node to be processed
        :type element: instance of lxml.html.HtmlElement
        :returns: the URL of the iframe to be lazy loaded
        :rtype: str
        """
        assert element.tag == 'iframe'
        if 'src' not in element.attrib:
            return  # `src` attribute is optional for <iframe> tags
        element.attrib['data-src'] = element.attrib['src']
        del element.attrib['src']
        return element.attrib['data-src']

    def _lazyload_tweet(self, element):
        """Process tweets for lazy loading. Twitter describes tweets
        using <blockquote> tags with a `twitter-tweet` class and loads
        a widget in a sibling <script> tag. To lazy load we need to add
        a `data-twitter` attribute and remove the widget.

        :param element: the HTML node to be processed
        :type element: instance of lxml.html.HtmlElement
        :returns: the URL of the tweet to be lazy loaded
        :rtype: str
        """
        assert element.tag == 'blockquote'
        # processing a tweet is tricky and prone to errors
        # abort at any time if the user has modified the code
        element.attrib['data-twitter'] = 'twitter-tweet'
        # remove sibling <script> tag to avoid an useless request
        sibling = element.getnext()
        if sibling is None:
            return  # Twitter's embed code was somehow modified, abort
        widget = '//platform.twitter.com/widgets.js'
        if sibling.tag == 'script' and widget in sibling.attrib['src']:
            parent = element.getparent()
            parent.remove(sibling)
            logger.debug("Twitter's widget <script> tag removed")
        try:
            return element.find('a').attrib['href']
        except AttributeError:
            return  # Twitter's embed code was somehow modified, abort

    def _lazyload(self, element):
        """Inject attributes needed by lazysizes to lazy load elements.
        For more information, see: https://afarkas.github.io/lazysizes
        """
        assert element.tag in ('img', 'iframe', 'blockquote')

        classes = element.attrib.get('class', '').split(' ')
        if 'lazyload' in classes:
            return  # this should never happen

        if element.tag == 'img':
            src = self._lazyload_img(element)
        elif element.tag == 'iframe':
            src = self._lazyload_iframe(element)
        elif element.tag == 'blockquote':
            if 'twitter-tweet' not in classes:
                return  # not a tweet
            src = self._lazyload_tweet(element)
            if src is not None:
                classes.remove('twitter-tweet')

        if src is None:
            return  # something went wrong or lazy load not needed

        classes.append('lazyload')
        element.attrib['class'] = ' '.join(classes).strip()
        msg = u'<{0}> tag with src="{1}" was processed for lazy loading'
        logger.debug(msg.format(element.tag, src))

    def _blacklist(self, result, blacklisted_classes):
        """Return a list of blacklisted elements."""
        if not blacklisted_classes:
            return ()

        path = []
        for css_class in blacklisted_classes:
            path.append('{0}{1}//img|{0}{1}//iframe|{0}{1}//blockquote'.format(
                ROOT_SELECTOR, CLASS_SELECTOR.format(css_class)))

        path = '|'.join(path)
        return result.tree.xpath(path)

    def transformBytes(self, result, encoding):
        return

    def transformUnicode(self, result, encoding):
        return

    def transformIterable(self, result, encoding):
        if not api.user.is_anonymous():
            return

        result = self._parse(result)
        if result is None:
            return

        record = ILazySizesSettings.__identifier__ + '.css_class_blacklist'
        blacklist = api.portal.get_registry_record(record)
        blacklist = self._blacklist(result, blacklist)

        path = '{0}//img|{0}//iframe|{0}//blockquote'.format(ROOT_SELECTOR)
        for el in result.tree.xpath(path):
            if el in blacklist:
                continue
            self._lazyload(el)

        return result
