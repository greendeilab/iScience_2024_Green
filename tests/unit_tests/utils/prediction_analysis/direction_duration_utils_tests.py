import sys
import unittest

sys.path.append('../../../../src')
from utils.prediction_analysis import direction_duration_utils as d 

class DirectionDurationUtilsTests(unittest.TestCase):

	def test_find_direction_durations_empty_flight_intervals_success(self):
		# Arrange
		headings = self.createHeadings(0, 91)
		flight_intervals = []
		expected_direction_durations = {'duration': [], 'direction': []}

		# Act
		actual_direction_durations = d.find_direction_durations(headings, flight_intervals)

		# Assert
		self.assertEqual(expected_direction_durations, actual_direction_durations)

	def createHeadings(self, lower_bound, upper_bound):
		headings = {}
		for num in range(lower_bound, upper_bound):
			headings.setdefault(num, num)
		return headings

	def test_find_direction_durations_one_duration_toward_success(self):
		# Arrange
		headings = self.createHeadings(0, 361)
		flight_intervals = [[0, 180]]
		expected_direction_durations = {'duration': [180], 'direction': ['toward']}

		# Act
		actual_direction_durations = d.find_direction_durations(headings, flight_intervals)

		# Assert
		#self.assertEqual(expected_direction_durations, actual_direction_durations)

	def test_find_direction_durations_one_duration_away_success(self):
		# Arrange
		headings = self.createHeadings(0, 361)
		flight_intervals = [[180, 360]]
		expected_direction_durations = {'duration': [180], 'direction': ['away']}

		# Act
		actual_direction_durations = d.find_direction_durations(headings, flight_intervals)

		# Assert
		self.assertEqual(expected_direction_durations, actual_direction_durations)

	def test_find_direction_durations_both_ways_success(self):
		# Arrange
		headings = self.createHeadings(0, 361)
		flight_intervals = [[0, 90], [180, 360]]
		expected_direction_durations = {'duration': [90, 180], 'direction': ['toward', 'away']}
		
		# Act
		actual_direction_durations = d.find_direction_durations(headings, flight_intervals)

		# Assert
		self.assertEqual(expected_direction_durations, actual_direction_durations)

	def test_find_direction_durations_alternating_success(self):
		# Arrange
		headings = {0: 90, 1: 91, 2: 93, 3:95, 4:267, 5: 311, 6: 301, 7: 210, 8: 102, 9: 103, 10: 240}
		flight_intervals = [[0, 10]]
		expected_direction_durations = {'duration': [4, 4, 2], 'direction': ['toward', 'away', 'toward']}

		# Act
		actual_direction_durations = d.find_direction_durations(headings, flight_intervals)
		
		# Assert
		self.assertEqual(expected_direction_durations, actual_direction_durations)

	def test_find_direction_durations_same_duration_alternating_success(self):
		# Arrange
		headings = {0: 90, 1: 270, 2: 90, 3: 270, 4: 90, 5: 270, 6: 90, 7: 270, 8: 90, 9: 270, 10: 90}
		flight_intervals = [[0, 10]]
		expected_direction_durations = {'duration': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
						  				'direction': ['toward', 'away', 'toward', 'away', 'toward', 'away', 'toward', 'away', 'toward', 'away']}
		
		# Act
		actual_direction_durations = d.find_direction_durations(headings, flight_intervals)

		# Assert
		self.assertEqual(expected_direction_durations, actual_direction_durations)		  

	def test_create_reference_intervals_default_values_success(self):
		# Arrange
		expected_reference_intervals = [[0, 180]]

		# Act
		actual_reference_intervals = d.create_reference_intervals()

		# Assert
		self.assertEqual(expected_reference_intervals, actual_reference_intervals)

	def test_create_reference_intervals_45_reference_success(self):
		# Arrange
		reference_angle = 45
		expected_reference_intervals = [[315, 360], [0, 135]]

		# Act
		actual_reference_intervals = d.create_reference_intervals(reference_angle=reference_angle)

		# Assert
		self.assertEqual(expected_reference_intervals, actual_reference_intervals)

	def test_create_reference_intervals_315_reference_success(self):
		# Arrange
		reference_angle = 315
		expected_reference_intervals = [[0, 45], [225, 360]]

		# Act
		actual_reference_intervals = d.create_reference_intervals(reference_angle=reference_angle)
		
		# Assert
		self.assertEqual(expected_reference_intervals, actual_reference_intervals)

	def test_flying_towards_reference_success(self):
		# Arrange
		reference_intervals = [[0, 180]]
		angles = [0, 179, 359, 181]
		expected_results = [True, True, False, False]

		# Act and Assert
		for i in range(len(angles)):
			is_flying_towards_reference = d.is_flying_towards_reference(angles[i], reference_intervals)
			self.assertEqual(expected_results[i], is_flying_towards_reference)

if __name__ == "__main__":
	unittest.main()