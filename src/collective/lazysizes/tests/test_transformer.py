# -*- coding: utf-8 -*-
from collective.lazysizes.testing import INTEGRATION_TESTING
from collective.lazysizes.transform import LazySizesTransform

import lxml
import unittest


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
        self.transformer = LazySizesTransform(None, request)

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

    def test_lazyload_img_no_src(self):
        element = lxml.html.fromstring('<img />')
        # the transformer returns None (skip element)
        self.assertIsNone(self.transformer._lazyload_img(element))

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
