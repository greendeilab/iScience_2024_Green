import sys
import unittest

sys.path.append('../../../src')
from utils import general_algorithms as g

class GeneralAlgorithmsTests(unittest.TestCase):
		
	def test_binary_search_default_target_found(self):
		# Arrange
		array = [0, 4, 5, 8, 9, 10]

		# Act
		indices = [g.binary_search(value, array) for value in array]

		# Assert
		for i in range(len(array)):
			self.assertEqual(i, indices[i])

	def test_binary_search_default_target_not_found(self):
		# Arrange
		array = [0, 4, 5, 8, 9, 10]
		targets = [-1, 1, 6, 11]
		expected_indices = [-1, -2, -4, -7] 

		# Act
		indices = [g.binary_search(target, array) for target in targets]

		# Assert
		for i in range(len(targets)):
			self.assertEqual(expected_indices[i], indices[i])

	def test_binary_search_custom_func_target_found(self):
		# Arrange
		tuples = [(0, 1), (4, 5), (5, 6), (8, 9), (9, 10), (10, 11)]

		# Act
		indices = [g.binary_search(tuple_[1], tuples, self.compare_end_tuple) for tuple_ in tuples]

		# Assert
		for i in range(len(tuples)):
			self.assertEqual(i, indices[i])

	def compare_end_tuple(self, tuple_, target):
		if target < tuple_[1]:
			return -1
		elif target == tuple_[1]:
			return 0
		else:
			return 1

	def test_binary_search_custom_func_not_found(self):
		# Arrange
		tuples = [(0, 1), (4, 5), (5, 6), (8, 9), (9, 10), (10, 11)]
		targets = [-1, 2, 7, 12]
		expected_indices = [-1, -2, -4, -7]

		# Act
		indices = [g.binary_search(target, tuples, self.compare_end_tuple) for target in targets]

		# Assert
		for i in range(len(targets)):
			self.assertEqual(expected_indices[i], indices[i])

if __name__ == "__main__":
	unittest.main()