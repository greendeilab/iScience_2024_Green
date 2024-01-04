import sys
import unittest
import numpy as np

sys.path.append('../../../src')
from utils import compass_utils as c

class CompassUtilsTests(unittest.TestCase):

	def test_calculate_north_angles_success(self):
		# Arrange
		label_map = {'origin': 0, 'north': 1}
		predictions = {0: np.array([[100, 100, 100, 100, 0.95, 0], [50, 150, 50, 150, 0.95, 1]]),
					   1: np.array([[100, 100, 100, 100, 0.95, 0], [45, 45, 45, 45, 0.95, 1]]),
					   2: np.array([[100, 100, 100, 100, 0.95, 0], [150, 150, 150, 150, 0.95, 1]]),
					   3: np.array([[100, 100, 100, 100, 0.95, 0], [45, 45, 45, 45, 0.95, 1]]),
					   4: np.array([[100, 100, 100, 100, 0.95, 0], [150, 50, 150, 50, 0.95, 1]])}

		# Act
		north_angles = c.calculate_north_angles(predictions, label_map)

		# Assert
		self.assertEqual([225, 135, 315, 135, 45], north_angles)

if __name__ == "__main__":
	unittest.main()