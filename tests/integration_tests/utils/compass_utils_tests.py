import sys
import unittest
import numpy as np
import os

sys.path.append('../../../src')
from utils import compass_utils as c

FILE_DIRECTORY = '../tests/integration_tests/files'

# Function names must be in camel case to be recognized by the unittest library
class CompassUtilsTests(unittest.TestCase):

	def setUp(self):
		if not os.path.exists(FILE_DIRECTORY):
			os.mkdir(FILE_DIRECTORY)

	def tearDown(self):
		for file in os.listdir(FILE_DIRECTORY):
			os.remove(f'{FILE_DIRECTORY}/{file}')

	def test_get_north_angle_multiple_predictions_success(self):
		# Arrange
		file_path = f'{FILE_DIRECTORY}/compass.npy'
		label_map = {'origin': 0, 'north': 1}
		predictions = np.array([{0: np.array([[100, 100, 100, 100, 0.95, 0], [45, 45, 45, 45, 0.95, 1]]),
								 1: np.array([[100, 100, 100, 100, 0.95, 0], [45, 45, 45, 45, 0.95, 1]]),
								 2: np.array([[100, 100, 100, 100, 0.95, 0], [45, 45, 45, 45, 0.95, 1]]),
								 3: np.array([[100, 100, 100, 100, 0.95, 0], [45, 45, 45, 45, 0.95, 1]]),
								 4: np.array([[100, 100, 100, 100, 0.95, 0], [150, 50, 150, 50, 0.95, 1]])}])
		self.save_compass_predictions(file_path, predictions)

		# Act
		north_angle = c.get_north_angle(file_path, label_map)

		# Assert
		self.assertEqual(135, north_angle)

	def save_compass_predictions(self, file_path, predictions):
		np.save(file_path, predictions, allow_pickle=True)

	def test_get_north_angle_empty_predictions_none(self):
		# Arrange
		file_path = f'{FILE_DIRECTORY}/compass.npy'
		label_map = {'origin': 0, 'north': 1}
		predictions = np.array([{0: np.array([[100, 100, 100, 100, 0.95, 0]]),
								 1: np.array([[100, 100, 100, 100, 0.95, 0]]),
								 2: np.array([[100, 100, 100, 100, 0.95, 0]]),
								 3: np.array([[100, 100, 100, 100, 0.95, 0]]),
								 4: np.array([[100, 100, 100, 100, 0.95, 0]])}])
		self.save_compass_predictions(file_path, predictions)

		# Act
		north_angle = c.get_north_angle(file_path, label_map)

		# Assert
		self.assertIsNone(north_angle)

if __name__ == "__main__":
	unittest.main()