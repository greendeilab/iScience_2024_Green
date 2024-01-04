import sys
import unittest

sys.path.append('../../../src')
from utils import trial_utils as t

class TrialUtilsTests(unittest.TestCase):

	def test_get_monarch_box_head_present_success(self):
		# Arrange
		locations = {'head': [1], 'body': [2]}

		# Act
		monarch_box = t.get_monarch_box(locations)

		# Assert
		self.assertEqual([1], monarch_box)

	def test_get_monarch_box_head_not_present_body_present_success(self):
		# Arrange
		locations = {'head': [], 'body': [2]}

		# Act
		monarch_box = t.get_monarch_box(locations)

		self.assertEqual([2], monarch_box)

	def test_get_monarch_box_head_nor_body_present_none(self):
		# Arrange
		locations = {'head': [], 'body': []}

		# Act
		monarch_box = t.get_monarch_box(locations)

		# Assert
		self.assertIsNone(monarch_box)

	def test_calculate_heading_all_north_success(self):
		for angle in range(0, 360, 10):
			# Arrange
			north_angle = angle
			heading = angle 

			# Act
			calibrated_angle = t.calibrate_to_north_angle(north_angle, heading)

			# Assert
			self.assertEqual(90, calibrated_angle)

	def test_calculate_heading_calibrated_angle_greater_360_success(self):
		# Arrange
		north_angle = 0 
		heading = 315

		# Act
		calibrated_angle = t.calibrate_to_north_angle(north_angle, heading)

		# Assert
		self.assertEqual(45, calibrated_angle)

	def test_calculate_heading_calibrated_angle_less_than_0_success(self):
		# Arrange
		north_angle = 315
		heading = 0

		# Act
		calibrated_angle = t.calibrate_to_north_angle(north_angle, heading)

		# Assert
		self.assertEqual(135, calibrated_angle)

	def test_get_corresponding_compass_file_file_present_success(self):
		# Arrange
		file = '20220914_102455_predictons_yolo.npy'
		north_angles = [
			['20220914_093320_predictions_yolo.npy', 0,],
			['20220914_102400_predictions_yolo.npy', 0],	# This is the ideal compass file
			['20220914_110000_predictions_yolo.npy', 0],
			['20220915_102455_predictions_yolo.npy', 0]
		]

		# Act
		compass_file = t.get_corresponding_compass_file(file, north_angles)

		# Assert
		self.assertEqual(1, compass_file)

	def test_get_corresponding_compass_file_file_not_present_assertion_raised(self):
		# Arrange
		file = '20220914_102455_predictons_yolo.npy'
		north_angles = [
			['20220914_093320_predictions_yolo.npy', 0],
			['20220914_102400_predictions_yolo.npy', 0],
			['20220914_110000_predictions_yolo.npy', 0],
			['20220915_102455_predictions_yolo.npy', 0]
		]

		# Act and Assert
		with self.assertRaises(AssertionError):
			t.get_corresponding_compass_file('20220920_102455_predictions_yolo.npy', north_angles)

if __name__ == "__main__":
	unittest.main()