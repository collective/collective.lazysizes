# -*- coding: utf-8 -*-
from collective.lazysizes.config import PROJECTNAME
from plone.app.upgrade.utils import loadMigrationProfile

import logging


def apply_profile(context):
    """Apply profile."""
    logger = logging.getLogger(PROJECTNAME)
    profile = 'profile-collective.lazysizes.upgrades.v2:default'
    loadMigrationProfile(context, profile)
    logger.info('Profile migrated.')
