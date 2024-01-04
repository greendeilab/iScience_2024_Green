import unittest
import sys

sys.path.append('../src')
from unit_tests.utils.angle_calculation_utils_tests import *
from unit_tests.utils.direction_duration_utils_tests import *
from unit_tests.utils.file_utils_tests import *
from unit_tests.utils.flight_interval_utils_tests import *
from unit_tests.utils.general_algorithms_tests import *
from unit_tests.utils.object_location_utils_tests import *
from unit_tests.utils.compass_utils_tests import *
from unit_tests.utils.statistics_utils_tests import *
from unit_tests.utils.trial_utils_tests import *

class UnitTestsTestSuite(unittest.TestSuite):

	def __init__(self):
		super().__init__()
		self.addTest(unittest.makeSuite(AngleCalculationUtilsTests))
		self.addTest(unittest.makeSuite(DirectionDurationUtilsTests))
		self.addTest(unittest.makeSuite(FileUtilsTests))
		self.addTest(unittest.makeSuite(FlightIntervalUtilsTests))
		self.addTest(unittest.makeSuite(GeneralAlgorithmsTests))
		self.addTest(unittest.makeSuite(ObjectLocationUtilsTests))
		self.addTest(unittest.makeSuite(CompassUtilsTests))
		self.addTest(unittest.makeSuite(StatisticsUtilsTests))
		self.addTest(unittest.makeSuite(TrialUtilsTests))




