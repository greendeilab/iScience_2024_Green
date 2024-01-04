import sys
import unittest
import math as m
import os 

sys.path.append('../../../src')
from utils import angle_calculation_utils as a 

class AngleCalculationUtilsTests(unittest.TestCase):

	def test_get_center_success(self):
		# Arrange
		box = [0, 0, 90, 90]
		expected_center = [45, 45]

		# Act
		actual_center = a.get_center(box)

		# Assert
		self.assertEqual(expected_center, actual_center)

	def test_calculate_box_centers_success(self):
		# Arrange
		box1 = [0, 0, 0, 0]
		box2 = [90, 90, 90, 90]
		expected_box_centers = [[0, 0], [90, 90]]

		# Act
		actual_box_centers = a.calculate_box_centers(box1, box2)

		# Assert
		self.assertEqual(expected_box_centers, actual_box_centers)

	def test_calculate_xy_difference_success(self):
		# Arrange
		box1 = [0, 0, 0, 0]
		box2 = [90, 90, 90, 90]
		expected_xy_difference = [-90, -90]

		# Act
		actual_xy_difference = a.calculate_xy_difference(box1, box2)

		# Assert
		self.assertEqual(expected_xy_difference, actual_xy_difference)

	def test_calculate_absolute_angle_success(self):
		# Arrange
		xys = [(0, 10), (0, -10), (5, 5), (5, -5), (10, 0)]
		expected_angles = [90, 90, 45, 45, 0]

		# Act
		actual_angles = [a.calculate_absolute_angle(xy[0], xy[1]) for xy in xys]

		# Assert
		self.assertEqual(expected_angles, actual_angles)

	def test_calculate_image_quadrant_quadrant1_success(self):
		# Arrange
		xys = [(0, 0), (5, -2), (0, -2)]

		# Act and Assert
		func = lambda xy: a.calculate_image_quadrant(xy[0], xy[1])
		self.assert_same_value_for_all(1, xys, func)

	def assert_same_value_for_all(self, value, array, func):
		for obj in array:
			self.assertEqual(value, func(obj))	

	def test_calculate_image_quadrant_quadrant2_success(self):
		# Arrange
		xys = [(-5, -2), (-5, 0)]

		# Act and Assert
		func = lambda xy: a.calculate_image_quadrant(xy[0], xy[1])
		self.assert_same_value_for_all(2, xys, func)

	def test_calculate_image_quadrant_quadrant3_success(self):
		# Arrange
		xys = [(-5, 2)]

		# Act and Assert
		func = lambda xy: a.calculate_image_quadrant(xy[0], xy[1])
		self.assert_same_value_for_all(3, xys, func)

	def test_calculate_image_quadrant_quadrant4_success(self):
		# Arrange
		xys = [(5, 2), (0, 2)]

		# Act and Assert
		func = lambda xy: a.calculate_image_quadrant(xy[0], xy[1])
		self.assert_same_value_for_all(4, xys, func)

	def test_calculate_normal_quadrant_quadrant1_success(self):
		# Arrange
		xys = [(0, 0), (5, 2), (0, 2)]

		# Act and Assert
		func = lambda xy: a.calculate_normal_quadrant(xy[0], xy[1])
		self.assert_same_value_for_all(1, xys, func)

	def test_calculate_normal_quadrant_quadrant2_success(self):
		# Arrange
		xys = [(-5, 2), (-5, 0)]

		# Act and Assert
		func = lambda xy: a.calculate_normal_quadrant(xy[0], xy[1])
		self.assert_same_value_for_all(2, xys, func)

	def test_calculate_normal_quadrant_quadrant3_success(self):
		# Arrange
		xys = [(-5, -2)]

		# Act and Assert
		func = lambda xy: a.calculate_normal_quadrant(xy[0], xy[1])
		self.assert_same_value_for_all(3, xys, func)

	def test_calculate_normal_quadrant_quadrant4_success(self):
		# Arrange
		xys = [(5, -2), (0, -2)]

		# Act and Assert
		func = lambda xy: a.calculate_normal_quadrant(xy[0], xy[1])
		self.assert_same_value_for_all(4, xys, func)

	def test_correct_angle_based_on_quadrant_success(self):
		# Arrange
		angles = [90, 45, 0, 45, 90, 45]
		quadrants = [1, 2, 2, 3, 4, 4]
		expected_corrected_angles = [90, 135, 180, 225, 270, 315]

		# Act
		actual_corrected_angles = []
		for i in range(len(angles)):
			angle = angles[i]
			quadrant = quadrants[i]
			result = a.correct_angle_based_on_quadrant(angle, quadrant)
			actual_corrected_angles.append(result)

		# Assert
		self.assertEqual(expected_corrected_angles, actual_corrected_angles)

	def test_calculate_random_boxes_success(self):
		# Act and Assert
		for expected_angle in range(0, 360, 45):
			box_interest, box_reference = self.createTestBoxes(expected_angle)
			self.assertEqual(expected_angle, a.calculate(box_interest, box_reference))

	def createTestBoxes(self, expected_angle):
		constant = 100
		box_interest = []
		box_reference = [constant, constant, constant, constant]
		expected_angle_radians = m.radians(expected_angle)
		x = constant + int(m.cos(expected_angle_radians) * 100)
		y = constant - int(m.sin(expected_angle_radians) * 100)
		box_interest = [x, y, x, y]
		return box_interest, box_reference

if __name__ == "__main__":
	unittest.main()