import sys
import unittest
import numpy as np

sys.path.append('../../../../src')
from utils.image_extraction import problematic_frame_utils as p 

class ProblematicFrameUtilsTests(unittest.TestCase):

	def test_find_problems_no_problems_detected(self):
		# Arrange
		num_unique_objects = 3
		predictions = {1: np.array([[0, 0, 0, 0, 0.9, 0], 
						   			[0, 0, 0, 0, 0.9, 1],
						   			[0, 0, 0, 0, 0.9, 2]])}

		expected = [[], []]

		# Act
		actual = p.find_problems(predictions, num_unique_objects)

		# Assert
		self.assertEqual(expected, actual)

	def test_find_problems_duplicate_objects_detected(self):
		# Arrange
		num_unique_objects = 3
		predictions = {1: np.array([[0, 0, 0, 0, 0.9, 0], 
						   			[0, 0, 0, 0, 0.9, 1],
						   			[0, 0, 0, 0, 0.9, 1],
						   			[0, 0, 0, 0, 0.9, 2]])}

		expected = [[1], []]
		
		# Act
		actual = p.find_problems(predictions, num_unique_objects)

		# Assert
		self.assertEqual(expected, actual)

	def test_find_problems_missing_objects_detected(self):
		# Arrange
		num_unique_objects = 3
		predictions = {1: np.array([[0, 0, 0, 0, 0.9, 0], 
						   			[0, 0, 0, 0, 0.9, 1]])}

		expected = [[], [1]]

		# Act
		actual = p.find_problems(predictions, num_unique_objects)

		# Assert
		self.assertEqual(expected, actual)

	def test_has_duplicate_objects_true(self):
		# Arrange
		labels = np.array([0, 1, 1])

		# Act
		has_duplicate_objects = p.has_duplicate_objects(labels)

		# Assert
		self.assertTrue(has_duplicate_objects)

	def test_has_duplicate_objects_false(self):
		# Arrange
		labels = np.array([0, 1, 2])

		# Act
		has_duplicate_objects = p.has_duplicate_objects(labels)

		# Assert
		self.assertFalse(has_duplicate_objects)

if __name__ == "__main__":
	unittest.main()