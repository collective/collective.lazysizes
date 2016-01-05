# -*- coding: utf-8 -*-
from plone.app.imaging.utils import getAllowedSizes
from zope.schema.vocabulary import SimpleVocabulary


def ImageScalesVocabulary(context):
    """Return a vocabulary listing all image scales.

    An example item would have token set to 'tile (64, 64)' and
    value to ('tile', 64, 64).
    """
    terms = []
    for name, size in getAllowedSizes().iteritems():
        terms.append(SimpleVocabulary.createTerm(
            tuple((name,) + size), str(name), u'{0} {1}'.format(name, size)))
    return SimpleVocabulary(terms)
