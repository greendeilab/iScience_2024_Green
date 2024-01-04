import sys
import unittest
import os
import openpyxl as op 
import numpy as np

sys.path.append('../../../src')
from utils import flight_interval_utils as f

class FlightIntervalUtilsTests(unittest.TestCase):

	def test_calculate_body_areas_success(self):
		# Arrange
		body_boxes = [[0, 0, 4, 4], [0, 0, 5, 5]]
		expected_body_areas = [16, 25]

		# Act
		actual_body_areas = f.calculate_body_areas(body_boxes)

		# Assert
		self.assertEqual(expected_body_areas, actual_body_areas)

	def test_calculate_area_area_greater_than_0_success(self):
		# Arrange
		box = [0, 0, 5, 5]

		# Act
		area = f.calculate_area(box)

		# Assert
		self.assertEqual(25, area)

	def test_calculate_area_area_equal_to_0_success(self):
		# Arrange
		box = [0, 0, 0, 0]

		# Act
		area = f.calculate_area(box)

		# Assert
		self.assertEqual(0, area)

	def test_calculate_body_fluctuations_success(self):
		# Arrange
		seconds = [0, 0.5, 1, 1.5, 2]
		body_areas = [25, 21, 29, 25, 27]
		expected_body_fluctuations = [-8, 16, -8, 4]

		# Act
		actual_body_fluctuations = f.calculate_body_fluctuations(seconds, body_areas)

		# Assert
		self.assertEqual(expected_body_fluctuations, actual_body_fluctuations)

	def test_find_time_of_claps_claps_present_success(self):
		# Arrange
		seconds = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
		body_areas = [10000, 1000, 100, 0, 100, 1000, 10000]
		body_fluctuations = [10000, -10000, -30000, 0, 30000, 10000, -10000]
		expected_time_of_claps = [0.3]

		# Act
		actual_time_of_claps = f.find_time_of_claps(seconds, body_areas, body_fluctuations)

		# Assert
		self.assertEqual(expected_time_of_claps, actual_time_of_claps)

	def test_ith_area_is_local_min_true(self):
		# Arrange
		body_areas = [10000, 1000, 100, 0, 100, 1000, 10000]
		i = 3

		# Act
		ith_area_is_local_min = f.ith_area_is_local_min(i, body_areas)

		# Assert
		self.assertTrue(ith_area_is_local_min)

	def test_ith_area_is_local_min_false(self):
		# Arrange
		body_areas = [10000, 1000, 100, 101, 100, 1000, 10000]
		i = 3

		# Act
		ith_area_is_local_min = f.ith_area_is_local_min(i, body_areas)

		# Assert
		self.assertFalse(ith_area_is_local_min)

	def test_body_is_active_true(self):
		# Arrange
		body_fluctuations = [10000, -10000, -30000, 0, 30000, 10000, -10000]
		i = 3

		# Act
		body_is_active = f.body_is_active(i, body_fluctuations)

		# Assert
		self.assertTrue(body_is_active)

	def test_body_is_active_false(self):
		# Arrange
		body_fluctuations = [10000, -10000, -500, 1000, 500, 10000, -10000]
		i = 3

		# Act
		body_is_active = f.body_is_active(i, body_fluctuations)

		# Assert
		self.assertFalse(body_is_active)

	def test_find_flight_intervals_interval_present_success(self):
		'''
			Some might consider 1.7 to be the end of the interval but the 
			algorithm takes a conservative approach and stops at the first sign of slowing down
		'''
		# Arrange
		time_of_claps = [1.3, 1.35, 1.4, 1.45, 1.5, 1.55, 1.6, 1.7, 2.2, 2.3, 5, 5.5, 6]
		expected_flight_intervals = [(1.3, 1.6)]		

		# Act
		actual_flight_intervals = f.find_flight_intervals(time_of_claps)

		# Assert
		self.assertEqual(expected_flight_intervals, actual_flight_intervals)

	def test_find_flight_intervals_interval_not_present_success(self):
		# Arrange
		time_of_claps = [1.3, 1.8, 1.9, 2.0, 2.5, 2.8, 5, 5.5, 6]
		expected_flight_intervals = []

		# Act
		actual_flight_intervals = f.find_flight_intervals(time_of_claps)

		# Assert
		self.assertEqual(expected_flight_intervals, actual_flight_intervals)

	def test_find_num_claps_before_and_after_start_claps_success(self):
		# Arrange
		time_of_claps = [0, 0.1, 0.5, 1, 1.6, 1.8, 2.0, 2.5, 2.7, 3.0]
		i = 0

		# Act
		[num_claps_before, num_claps_after] = f.find_num_claps_before_and_after(i, time_of_claps)

		# Assert
		self.assertEqual(0, num_claps_before)
		self.assertEqual(2, num_claps_after)

	def test_find_num_claps_before_and_after_middle_claps_success(self):
		# Arrange
		time_of_claps = [0, 0.1, 0.5, 1, 1.6, 1.8, 2.0, 2.5, 2.7, 3.0]
		i = 5

		# Act
		[num_claps_before, num_claps_after] = f.find_num_claps_before_and_after(i, time_of_claps)

		# Assert
		self.assertEqual(2, num_claps_before)
		self.assertEqual(3, num_claps_after)

	def test_find_num_claps_before_and_after_end_claps_success(self):
		# Arrange
		time_of_claps = [0, 0.1, 0.5, 1, 1.6, 1.8, 2.0, 2.5, 2.7, 3.0]
		i = len(time_of_claps) - 1

		# Act
		[num_claps_before, num_claps_after] = f.find_num_claps_before_and_after(i, time_of_claps)

		# Assert
		self.assertEqual(2, num_claps_before)
		self.assertEqual(0, num_claps_after)

	def test_is_start_interval_true(self):
		# Arrange
		num_claps_before = 0
		num_claps_after = 6

		# Act
		is_start_interval = f.is_start_interval(num_claps_before, num_claps_after)

		# Assert
		self.assertTrue(is_start_interval)

	def test_is_start_interval_false(self):
		# Arrange
		num_claps_before = 6
		num_claps_after = 6

		# Act
		is_start_interval = f.is_start_interval(num_claps_before, num_claps_after)

		# Assert
		self.assertFalse(is_start_interval)

	def test_is_end_interval_true(self):
		# Arrange
		num_claps_before = 6
		num_claps_after = 0

		# Act
		is_end_interval = f.is_end_interval(num_claps_before, num_claps_after)

		# Assert
		self.assertTrue(is_end_interval)	

	def test_is_end_interval_false(self):
		# Arrange
		num_claps_before = 6
		num_claps_after = 6

		# Act
		is_end_interval = f.is_end_interval(num_claps_before, num_claps_after)

		# Assert
		self.assertFalse(is_end_interval)

	def test_is_flight_interval_true(self):
		# Arrange
		flight_interval = (4, 10)

		# Act
		is_flight_interval = f.is_flight_interval(flight_interval)

		# Assert
		self.assertTrue(is_flight_interval)

	def test_is_flight_interval_no_start_false(self):
		# Arrange
		flight_interval = (-1, 5)

		# Act
		is_flight_interval = f.is_flight_interval(flight_interval)

		# Assert
		self.assertFalse(is_flight_interval)

	def test_is_flight_interval_no_end_false(self):
		# Arrange
		flight_interval = (5, -1)

		# Act
		is_flight_interval = f.is_flight_interval(flight_interval)

		# Assert
		self.assertFalse(is_flight_interval)


	def test_filter_flight_intervals_success(self):
		# Arrange
		flight_intervals = [(0, 1.5), (4, 8.9), (10, 12.5)]

		# Act
		filtered_flight_intervals = f.filter_flight_intervals(flight_intervals, 4)

		# Assert
		self.assertEqual(1, len(filtered_flight_intervals))
		self.assertEqual(flight_intervals[1], filtered_flight_intervals[0])

	def test_is_start_flight_interval_true(self):
		# Arrange
		flight_intervals = [(0, 1.5), (4, 8.9), (10, 12.5)]

		# Act
		is_start_of_flight_interval = f.is_start_of_flight_interval(10, flight_intervals)

		# Assert 
		self.assertTrue(is_start_of_flight_interval)

	def test_is_start_flight_interval_false(self):
		# Arrange
		flight_intervals = [(0, 1.5), (4, 8.9), (10, 12.5)]

		# Act
		is_start_of_flight_interval = f.is_start_of_flight_interval(3, flight_intervals)

		# Assert 
		self.assertFalse(is_start_of_flight_interval)

	def test_is_during_flight_interval_on_start_boundary_true(self):
		# Arrange
		flight_intervals = [(0, 1.5), (4, 8.9), (10, 12.5)]

		# Act
		is_start_of_flight_interval = f.is_during_flight_interval(4, flight_intervals)

		# Assert 
		self.assertTrue(is_start_of_flight_interval)

	def test_is_during_flight_interval_on_end_boundary_true(self):
		# Arrange
		flight_intervals = [(0, 1.5), (4, 8.9), (10, 12.5)]

		# Act
		is_start_of_flight_interval = f.is_during_flight_interval(4, flight_intervals)

		# Assert 
		self.assertTrue(is_start_of_flight_interval)

	def test_is_during_flight_interval_between_boundaries_true(self):
		# Arrange
		flight_intervals = [(0, 1.5), (4, 8.9), (10, 12.5)]

		# Act
		is_start_of_flight_interval = f.is_during_flight_interval(5, flight_intervals)

		# Assert 
		self.assertTrue(is_start_of_flight_interval)

	def test_is_during_flight_interval_false(self):
		# Arrange
		flight_intervals = [(0, 1.5), (4, 8.9), (10, 12.5)]

		# Act
		is_start_of_flight_interval = f.is_during_flight_interval(3.6, flight_intervals)

		# Assert 
		self.assertFalse(is_start_of_flight_interval)

	def test_is_end_of_flight_interval_true(self):
		# Arrange
		flight_intervals = [(0, 1.5), (4, 8.9), (10, 12.5)]

		# Act
		is_end_flight_interval = f.is_end_of_flight_interval(8.9, flight_intervals)

		# Assert 
		self.assertTrue(is_end_flight_interval)

	def test_end_flight_interval_false(self):
		# Arrange
		flight_intervals =  [(0, 1.5), (4, 8.9), (10, 12.5)]

		# Act
		is_end_flight_interval = f.is_end_of_flight_interval(8, flight_intervals)

		# Assert
		self.assertFalse(is_end_flight_interval)

if __name__ == "__main__":
	unittest.main()