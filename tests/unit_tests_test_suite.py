import unittest
import sys

sys.path.append('../src')
from unit_tests.utils.prediction_analysis.angle_calculation_utils_tests import *
from unit_tests.utils.prediction_analysis.direction_duration_utils_tests import *
from unit_tests.utils.prediction_analysis.flight_interval_utils_tests import *
from unit_tests.utils.prediction_analysis.compass_utils_tests import *
from unit_tests.utils.prediction_analysis.statistics_utils_tests import *
from unit_tests.utils.prediction_analysis.trial_utils_tests import *

from unit_tests.utils.image_extraction.video_utils_tests import *
from unit_tests.utils.image_extraction.problematic_frame_utils_tests import *

from unit_tests.utils.file_utils_tests import *
from unit_tests.utils.general_algorithms_tests import *
from unit_tests.utils.object_location_utils_tests import *

from unit_tests.orchestrators.image_extraction_test_suite import *

class UnitTestsTestSuite(unittest.TestSuite):

	def __init__(self):
		super().__init__()
		self.addTest(unittest.makeSuite(AngleCalculationUtilsTests))
		self.addTest(unittest.makeSuite(DirectionDurationUtilsTests))
		self.addTest(unittest.makeSuite(FlightIntervalUtilsTests))
		self.addTest(unittest.makeSuite(CompassUtilsTests))
		self.addTest(unittest.makeSuite(StatisticsUtilsTests))
		self.addTest(unittest.makeSuite(TrialUtilsTests))

		self.addTest(unittest.makeSuite(VideoUtilsTests))
		self.addTest(unittest.makeSuite(ProblematicFrameUtilsTests))

		self.addTest(unittest.makeSuite(FileUtilsTests))
		self.addTest(unittest.makeSuite(GeneralAlgorithmsTests))
		self.addTest(unittest.makeSuite(ObjectLocationUtilsTests))

		self.addTest(unittest.makeSuite(ImageExtractionOrchestrator))




