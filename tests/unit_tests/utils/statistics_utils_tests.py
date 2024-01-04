import sys
import unittest

sys.path.append('../../../src')
from utils import statistics_utils as s

class StatisticsUtilsTests(unittest.TestCase):

	def test_get_total_frames_success(self):
		# Arrange
		predictions = {1: [], 2: [], 3: [], 4: []}

		# Act
		total_frames = s.get_total_frames(predictions)

		# Assert
		self.assertEqual(4, total_frames)

	def test_get_frames_identified_success(self):
		# Arrange
		all_object_locations = {1: [], 2:[], 3: []}

		# Act
		frames_identified = s.get_frames_identified(all_object_locations)

		# Assert
		self.assertEqual(3, frames_identified)
	
	def test_calculate_total_flying_time_success(self):
		# Arrange
		flight_intervals = [(0, 5.5), (10, 15.5)]
		
		# Act
		total_flying_time = s.calculate_total_flying_time(flight_intervals)

		# Assert
		self.assertEqual(11, total_flying_time)

	def test_calculate_xy_success(self):
		# Arrange
		headings = [{0: 0}, {0: 90}, {0: 180}, {0: 270}, {0: 360}]
		expected_xys = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 0)]

		# Act and Assert
		for i in range(len(headings)):
			x, y = s.calculate_xy(headings[i])
			self.assertEqual(expected_xys[i][0], round(x, 6))			# Have to round to prevent rounding issues
			self.assertEqual(expected_xys[i][1], round(y, 6))

	def test_calculate_average_r_success(self):
		# Arrange
		xys = [(3, 0), (0, 3), (3, 4)]
		expected_average_rs = [3, 3, 5]

		# Act and Assert
		for i in range(len(xys)):
			self.assertEqual(expected_average_rs[i], s.calculate_average_r(xys[i][0], xys[i][1]))

	def test_calculate_average_theta_success(self):
		# Arrange
		xys = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
		expected_average_thetas = [0, 45, 90, 135, 180, 225, 270, 315]
		
		# Act and Assert
		for i in range(len(xys)):
			self.assertEqual(expected_average_thetas[i], s.calculate_average_theta(xys[i][0], xys[i][1]))

	def test_first_direction_success(self):
		# Arrange
		direction_durations = {'direction': ['toward', 'away', 'toward'],
								'duration': [1, 10, 5]}

		# Act
		first_direction = s.find_first_direction(direction_durations)

		# Assert
		self.assertEqual('toward', first_direction)

	def test_longest_consistent_direction(self):
		# Arrange
		direction_durations = {'direction': ['away', 'toward', 'away'],
								'duration': [9, 10, 8]}

		# Act
		longest_consistent_direction = s.find_longest_consistent_direction(direction_durations)
		
		# Assert
		self.assertEqual('toward', longest_consistent_direction)

	def test_calculate_total_flying_time_each_direction_no_flight_success(self):
		# Arrange
		direction_durations = {'direction': [], 'duration': []}
		expected_total_flying_time_each_direction = [0, 0]

		# Act
		actual_total_flying_time_each_direction = s.calculate_total_flying_time_each_direction(direction_durations)

		# Assert
		self.assertEqual(expected_total_flying_time_each_direction, actual_total_flying_time_each_direction)

	def test_calculate_total_flying_time_each_direction_flight_present_success(self):
		# Arrange
		direction_durations = {'direction': ['toward', 'away', 'toward', 'away'],
							   'duration': [0.05, 0.1, 0.05, 0.1]}
		expected_total_flying_time_each_direction = [0.1, 0.2]

		# Act
		actual_total_flying_time_each_direction = s.calculate_total_flying_time_each_direction(direction_durations)

		# Assert
		self.assertEqual(expected_total_flying_time_each_direction, actual_total_flying_time_each_direction)

	def test_find_first_consistent_direction_threshold_1_success(self):
		# Arrange
		direction_durations = {'direction': ['away', 'away', 'away', 'toward', 'away'],
								'duration': [1, 1, 1, 10, 8]}
		threshold = 1

		# Act
		first_consistent_direction =  s.find_first_consistent_direction(direction_durations, threshold)

		# Assert
		self.assertEqual('away', first_consistent_direction)

	def test_find_first_consistent_direction_threshold_2_success(self):
		# Arrange
		direction_durations = {'direction': ['away', 'away', 'away', 'toward', 'away'],
								'duration': [1, 1, 1, 10, 8]}
		threshold = 2

		# Act
		first_consistent_direction =  s.find_first_consistent_direction(direction_durations, threshold)

		# Assert
		self.assertEqual('toward', first_consistent_direction)

if __name__ == "__main__":
	unittest.main()