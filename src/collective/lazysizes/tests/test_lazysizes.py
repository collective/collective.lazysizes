# -*- coding: utf-8 -*-
from collective.lazysizes.config import IS_PLONE_5
from collective.lazysizes.testing import FUNCTIONAL_TESTING
from collective.lazysizes.transform import PLACEHOLDER
from plone import api
from plone.testing.z2 import Browser

import lxml
import transaction
import unittest


zptlogo = (
    'GIF89a\x10\x00\x10\x00\xd5\x00\x00\xff\xff\xff\xff\xff\xfe\xfc\xfd\xfd'
    '\xfa\xfb\xfc\xf7\xf9\xfa\xf5\xf8\xf9\xf3\xf6\xf8\xf2\xf5\xf7\xf0\xf4\xf6'
    '\xeb\xf1\xf3\xe5\xed\xef\xde\xe8\xeb\xdc\xe6\xea\xd9\xe4\xe8\xd7\xe2\xe6'
    '\xd2\xdf\xe3\xd0\xdd\xe3\xcd\xdc\xe1\xcb\xda\xdf\xc9\xd9\xdf\xc8\xd8\xdd'
    '\xc6\xd7\xdc\xc4\xd6\xdc\xc3\xd4\xda\xc2\xd3\xd9\xc1\xd3\xd9\xc0\xd2\xd9'
    '\xbd\xd1\xd8\xbd\xd0\xd7\xbc\xcf\xd7\xbb\xcf\xd6\xbb\xce\xd5\xb9\xcd\xd4'
    '\xb6\xcc\xd4\xb6\xcb\xd3\xb5\xcb\xd2\xb4\xca\xd1\xb2\xc8\xd0\xb1\xc7\xd0'
    '\xb0\xc7\xcf\xaf\xc6\xce\xae\xc4\xce\xad\xc4\xcd\xab\xc3\xcc\xa9\xc2\xcb'
    '\xa8\xc1\xca\xa6\xc0\xc9\xa4\xbe\xc8\xa2\xbd\xc7\xa0\xbb\xc5\x9e\xba\xc4'
    '\x9b\xbf\xcc\x98\xb6\xc1\x8d\xae\xbaFgs\x00\x00\x00\x00\x00\x00\x00\x00'
    '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    '\x00,\x00\x00\x00\x00\x10\x00\x10\x00\x00\x06z@\x80pH,\x12k\xc8$\xd2f\x04'
    '\xd4\x84\x01\x01\xe1\xf0d\x16\x9f\x80A\x01\x91\xc0ZmL\xb0\xcd\x00V\xd4'
    '\xc4a\x87z\xed\xb0-\x1a\xb3\xb8\x95\xbdf8\x1e\x11\xca,MoC$\x15\x18{'
    '\x006}m\x13\x16\x1a\x1f\x83\x85}6\x17\x1b $\x83\x00\x86\x19\x1d!%)\x8c'
    '\x866#\'+.\x8ca`\x1c`(,/1\x94B5\x19\x1e"&*-024\xacNq\xba\xbb\xb8h\xbeb'
    '\x00A\x00;'
)


def set_image_field(obj, image, content_type):
    """Set image field in object on both, Archetypes and Dexterity."""
    from plone.namedfile.file import NamedBlobImage
    try:
        obj.setImage(image)  # Archetypes
    except AttributeError:
        # Dexterity
        data = image if type(image) == str else image.getvalue()
        obj.image = NamedBlobImage(data=data, contentType=content_type)
    finally:
        obj.reindexObject()


class LazySizesTestCase(unittest.TestCase):

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.browser = Browser(self.layer['app'])

        with api.env.adopt_roles(['Manager']):
            self.image = api.content.create(
                self.portal, 'Image', id='test-image')

        set_image_field(self.image, image=zptlogo, content_type='image/gif')
        transaction.commit()

    def test_lazysizes_enabled_for_anonymous_user(self):
        self.browser.open(self.image.absolute_url() + '/view')
        html = lxml.html.fromstring(self.browser.contents)

        # main image was processed
        img = html.xpath('//img')[1]  # first image is the Plone logo
        self.assertEqual(PLACEHOLDER, img.attrib['src'])
        self.assertIn(self.image.absolute_url(), img.attrib['data-src'])
        self.assertEqual(img.attrib['class'], 'lazyload')

    @unittest.skipIf(IS_PLONE_5, 'Plone 4 only')
    def test_blacklist_plone_4(self):
        from collective.lazysizes.interfaces import ILazySizesSettings
        record = ILazySizesSettings.__identifier__ + '.css_class_blacklist'
        api.portal.set_registry_record(record, set(['discreet']))
        transaction.commit()

        self.browser.open(self.image.absolute_url() + '/view')
        html = lxml.html.fromstring(self.browser.contents)

        # main image was processed
        img = html.xpath('//img')[1]  # first image is the Plone logo
        self.assertEqual(PLACEHOLDER, img.attrib['src'])
        self.assertIn(self.image.absolute_url(), img.attrib['data-src'])
        self.assertEqual(img.attrib['class'], 'lazyload')

        # icons were not processed, but are present
        img = html.xpath('//img')[2]
        self.assertEqual('http://nohost/plone/search_icon.png', img.attrib['src'])
        self.assertNotIn('data-src', img.attrib)
        img = html.xpath('//img')[3]
        self.assertEqual('http://nohost/plone/download_icon.png', img.attrib['src'])
        self.assertNotIn('data-src', img.attrib)

    @unittest.skipIf(not IS_PLONE_5, 'Plone 5 only')
    def test_blacklist_plone_5(self):
        from collective.lazysizes.interfaces import ILazySizesSettings
        record = ILazySizesSettings.__identifier__ + '.css_class_blacklist'
        api.portal.set_registry_record(record, set(['discreet']))
        transaction.commit()

        self.browser.open(self.image.absolute_url() + '/view')
        html = lxml.html.fromstring(self.browser.contents)

        # main image was not processed
        img = html.xpath('//img')[1]  # first image is the Plone logo
        self.assertIn(self.image.absolute_url(), img.attrib['src'])
        self.assertNotIn('data-src', img.attrib)
