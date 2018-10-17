# -*- coding: utf-8 -*-
from collective.lazysizes.interfaces import ILazySizesSettings
from collective.lazysizes.testing import INTEGRATION_TESTING
from collective.lazysizes.transform import LazySizesTransform
from collective.lazysizes.transform import PLACEHOLDER
from plone import api
from plone.app.testing import logout
from plone.registry.interfaces import IRegistry
from testfixtures import log_capture
from zope.component import getUtility

import logging
import lxml  # nosec
import unittest


HTML = u"""<html>
  <body>
    <div id="content">
      <img src="{url}" class="{klass}" />
    </div>
  </body>
</html>
"""

TWEET = """
<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">Nothing Twitter is doing is working <a href="https://t.co/s0FppnacwK">https://t.co/s0FppnacwK</a> <a href="https://t.co/GK9MRfQkYO">pic.twitter.com/GK9MRfQkYO</a></p>&mdash; The Verge (@verge) <a href="https://twitter.com/verge/status/725096763972001794">April 26, 2016</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>
"""

TWEET_MODIFIED = """
<blockquote class="twitter-tweet" data-lang="en"></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>
"""

TWEET_NO_SCRIPT = """
<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">Nothing Twitter is doing is working <a href="https://t.co/s0FppnacwK">https://t.co/s0FppnacwK</a> <a href="https://t.co/GK9MRfQkYO">pic.twitter.com/GK9MRfQkYO</a></p>&mdash; The Verge (@verge) <a href="https://twitter.com/verge/status/725096763972001794">April 26, 2016</a></blockquote>
"""


class TransformerTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        request = self.layer['request']
        request.response.setHeader('Content-Type', 'text/html')
        self.transformer = LazySizesTransform(None, request)

    def test_transformer_anonymous_user(self):
        logout()
        url = 'http://example.com/foo.png'
        html = HTML.format(url=url, klass='')
        result = self.transformer.transformIterable(html, 'utf-8')
        img = result.tree.xpath('//img')[0]
        self.assertEqual(img.attrib['src'], PLACEHOLDER)
        self.assertEqual(img.attrib['class'], 'lazyload')
        self.assertIn(img.attrib['data-src'], url)

    def test_transformer_authenticated_user_disabled(self):
        url = 'http://example.com/foo.png'
        html = HTML.format(url=url, klass='')
        result = self.transformer.transformIterable(html, 'utf-8')
        self.assertIsNone(result)

    def test_transformer_authenticated_user_enabled(self):
        record = ILazySizesSettings.__identifier__ + '.lazyload_authenticated'
        api.portal.set_registry_record(record, True)
        url = 'http://example.com/foo.png'
        html = HTML.format(url=url, klass='')
        result = self.transformer.transformIterable(html, 'utf-8')
        img = result.tree.xpath('//img')[0]
        self.assertEqual(img.attrib['src'], PLACEHOLDER)
        self.assertEqual(img.attrib['class'], 'lazyload')
        self.assertIn(img.attrib['data-src'], url)

    def test_lazyload_img(self):
        url = 'http://example.com/foo.png'
        img_tag = '<img src="{0}" />'.format(url)
        element = lxml.html.fromstring(img_tag)
        # the transformer returns the URL of the referenced image
        self.assertEqual(self.transformer._lazyload_img(element), url)
        # the src attribute is the placeholder
        self.assertIn('src', element.attrib)
        self.assertTrue(element.attrib['src'].startswith('data:image/png'))
        # the data-src attribute is the original image
        self.assertIn('data-src', element.attrib)
        self.assertEqual(element.attrib['data-src'], url)

    @log_capture(level=logging.ERROR)
    def test_lazyload_img_no_src(self, l):
        element = lxml.html.fromstring('<img />')
        # the transformer returns None (skip element)
        self.assertIsNone(self.transformer._lazyload_img(element))

        # an error message must be logged
        msg = '<img> tag without src attribute in: http://nohost'
        expected = ('collective.lazysizes', 'ERROR', msg)
        l.check(expected)

    def test_lazyload_iframe(self):
        url = 'http://example.com/foo/bar'
        iframe_tag = '<iframe src="{0}" />'.format(url)
        element = lxml.html.fromstring(iframe_tag)
        # the transformer returns the URL of the referenced page
        self.assertEqual(self.transformer._lazyload_iframe(element), url)
        # the src attribute was removed
        self.assertNotIn('src', element.attrib)
        # the data-src attribute is the original page
        self.assertIn('data-src', element.attrib)
        self.assertEqual(element.attrib['data-src'], url)

    def test_lazyload_iframe_no_src(self):
        element = lxml.html.fromstring('<iframe />')
        # the transformer returns None (skip element)
        self.assertIsNone(self.transformer._lazyload_iframe(element))

    def test_lazyload_tweet(self):
        url = 'https://twitter.com/verge/status/725096763972001794'
        # get the blockquote tag only
        html = lxml.html.fromstring(TWEET)
        element = html.getchildren()[0]
        # the transformer returns the URL of the referenced tweet
        self.assertEqual(self.transformer._lazyload_tweet(element), url)
        # the data-twitter attribute was added
        self.assertIn('data-twitter', element.attrib)
        # the script tag was removed
        self.assertEqual(len(html.getchildren()), 1)

    def test_lazyload_tweet_modified(self):
        # get the blockquote tag only
        html = lxml.html.fromstring(TWEET_MODIFIED)
        element = html.getchildren()[0]
        # the transformer returns None (skip element)
        self.assertIsNone(self.transformer._lazyload_tweet(element))

    def test_lazyload_tweet_no_script(self):
        # get the blockquote tag only
        element = lxml.html.fromstring(TWEET_NO_SCRIPT)
        # the transformer returns None (skip element)
        self.assertIsNone(self.transformer._lazyload_tweet(element))

    @staticmethod
    def set_css_class_blacklist(value):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ILazySizesSettings)
        settings.css_class_blacklist = value

    def test_css_blacklisted_class(self):
        self.set_css_class_blacklist({'nolazyload'})
        logout()  # enable transform

        # Case 1: Do not transform Blacklisted - single class
        url = 'http://example.com/foo.png'
        klass = 'nolazyload'
        html = HTML.format(url=url, klass=klass)
        result = self.transformer.transformIterable(html, 'utf-8')
        img = result.tree.xpath('//img')[0]
        self.assertEqual(img.attrib['src'], url)
        self.assertEqual(img.attrib['class'], klass)
        self.assertNotIn('data-src', img.attrib)

    def test_css_blacklisted_multiple_classes(self):
        self.set_css_class_blacklist({'nolazyload'})
        logout()  # enable transform

        # Case 2: Do not transform Blacklisted - multiple classes
        url = 'http://example.com/foo.png'
        klass = 'nolazyload secondclass thirdclass'
        html = HTML.format(url=url, klass=klass)
        result = self.transformer.transformIterable(html, 'utf-8')
        img = result.tree.xpath('//img')[0]
        self.assertEqual(img.attrib['src'], url)
        self.assertEqual(img.attrib['class'], klass)
        self.assertNotIn('data-src', img.attrib)

    def test_css_blacklisted_false_possitives(self):
        self.set_css_class_blacklist({'nolazyload'})
        logout()  # enable transform

        # Case 3: Do not blacklist classes which contain the classname
        url = 'http://example.com/foo.png'
        klass = 'nolazyloadbutnot anothernolazyloadbutnot'
        html = HTML.format(url=url, klass=klass)
        result = self.transformer.transformIterable(html, 'utf-8')
        img = result.tree.xpath('//img')[0]
        self.assertEqual(img.attrib['src'], PLACEHOLDER)
        self.assertIn(klass, img.attrib['class'])
        self.assertIn('lazyload', img.attrib['class'])
        self.assertEqual(img.attrib['data-src'], url)
