import unittest
import sys

sys.path.append('../src')
from integration_tests.utils.file_utils_tests import *
from integration_tests.utils.compass_utils_tests import *

class IntegrationTestsTestSuite(unittest.TestSuite):

	def __init__(self):
		super().__init__()
		self.addTest(unittest.makeSuite(FileUtilsTests))
		self.addTest(unittest.makeSuite(CompassUtilsTests))




