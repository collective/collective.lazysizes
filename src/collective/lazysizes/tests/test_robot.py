# -*- coding: utf-8 -*-
from collective.lazysizes.testing import ROBOT_TESTING
from plone.testing import layered

import os
import robotsuite
import unittest


def test_suite():
    suite = unittest.TestSuite()
    current_dir = os.path.abspath(os.path.dirname(__file__))
    tests = [
        doc for doc in os.listdir(current_dir)
        if doc.startswith('test_') and doc.endswith('.robot')
    ]
    suite.addTests([
        layered(robotsuite.RobotTestSuite(t), layer=ROBOT_TESTING)
        for t in tests
    ])
    return suite
