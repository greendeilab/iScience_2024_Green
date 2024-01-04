import sys
import unittest
import os
import openpyxl as op 
import numpy as np

sys.path.append('../../../src')
from utils import file_utils as f

FPS = 120
FILE_DIRECTORY = '../tests/integration_tests/files'

# Some function names must be in camel case to be recognized by the unittest library
class FileUtilsTests(unittest.TestCase):

	def setUp(self):
		self.wb = op.Workbook()
		self.empty_sheet = self.wb.active
		self.all_trial_statistics = {'DATE_TIME_P1_predictions_yolo.npy' : {'stat_name': 0, 'long_stat_name': 0, 'stat_stat': 0}}

		if not os.path.exists(FILE_DIRECTORY):
			os.mkdir(FILE_DIRECTORY)

		self.test_file_names = ['compass.npy', 'COMPASS_.npy', 'file1.npy', 'file2.npy']
		for test_file_name in self.test_file_names:
			self.make_test_file(test_file_name)

	def make_test_file(self, test_file_name):
		np.save(f'{FILE_DIRECTORY}/{test_file_name}', np.array([0]), allow_pickle=True)

	def tearDown(self):
		existing_files =  os.listdir(FILE_DIRECTORY)
		for file in existing_files:
			os.remove(f'{FILE_DIRECTORY}/{file}')

	def test_open_prediction_file_success(self):
		# Arrange
		file_path = f'{FILE_DIRECTORY}/compass.npy'
		expected_file = np.load(file_path, allow_pickle=True).item()

		# Act
		actual_file = f.open_prediction_file(file_path)

		# Assert
		self.assertEqual(expected_file, actual_file)

	def test_open_prediction_file_as_trial_success(self):
		# Arrange
		file_path = f'{FILE_DIRECTORY}/prediction.npy'
		predictions = np.array([{0: np.array([[100, 100, 100, 100, 0.95, 0], [45, 45, 45, 45, 0.95, 1]]),
					 			 1: np.array([[100, 100, 100, 100, 0.95, 0], [45, 45, 45, 45, 0.95, 1]]),
					 			 2: np.array([[100, 100, 100, 100, 0.95, 0], [45, 45, 45, 45, 0.95, 1]]),
					 			 3: np.array([[100, 100, 100, 100, 0.95, 0], [45, 45, 45, 45, 0.95, 1]]),
					 			 4: np.array([[100, 100, 100, 100, 0.95, 0], [150, 50, 150, 50, 0.95, 1]])}])
		self.make_test_file_with_predictions(file_path, predictions)

		# Act
		opened_predictions, length_video = f.open_prediction_file_as_trial(file_path)

		# Assert
		self.assertEqual(4/FPS, length_video)
		for frame_num in predictions[0].keys():
			self.assertTrue(np.all(predictions[0][frame_num] == opened_predictions[frame_num / FPS]))

	def test_open_prediction_file_as_trial_and_trim_success(self):
		# Arrange
		file_path = f'{FILE_DIRECTORY}/prediction.npy'
		predictions = np.array([{0: np.array([[100, 100, 100, 100, 0.95, 0], [45, 45, 45, 45, 0.95, 1]]),
					 			 1: np.array([[100, 100, 100, 100, 0.95, 0], [45, 45, 45, 45, 0.95, 1]]),
					 			 2: np.array([[100, 100, 100, 100, 0.95, 0], [45, 45, 45, 45, 0.95, 1]]),
					 			 3: np.array([[100, 100, 100, 100, 0.95, 0], [45, 45, 45, 45, 0.95, 1]]),
					 			 4: np.array([[100, 100, 100, 100, 0.95, 0], [150, 50, 150, 50, 0.95, 1]])}])
		self.make_test_file_with_predictions(file_path, predictions)
		expected_length = 3 / FPS
		
		# Act
		opened_predictions, length_video = f.open_prediction_file_as_trial_and_trim(file_path, expected_length)

		# Assert
		self.assertEqual(expected_length, length_video)
		for frame_num in predictions[0].keys():
			if frame_num != 4:
				second = frame_num / FPS
				self.assertTrue(np.all(predictions[0][frame_num] == opened_predictions[second]))
			else:
				self.assertTrue(frame_num not in opened_predictions)

	def make_test_file_with_predictions(self, file_path, predictions):
		np.save(file_path, predictions, allow_pickle=True)

	def test_get_prediction_files_one_file_success(self):
		# Act
		files = f.get_prediction_files(FILE_DIRECTORY, True);

		# Assert
		self.assertEqual(2, len(files))
		
	def test_get_prediction_files_separate_files_success(self):
		# Act
		files = f.get_prediction_files(FILE_DIRECTORY, False);

		# Assert
		self.assertEqual(2, len(files))


	def test_get_compass_files_success(self):
		# Act
		files = f.get_compass_files(FILE_DIRECTORY)

		# Assert
		self.assertEqual(2, len(files))
		self.assertTrue('compass.npy' in files)
		self.assertTrue('COMPASS_.npy' in files)
		
	def test_get_all_trial_files_files_present_success(self):
		# Act
		files = f.get_trial_files(FILE_DIRECTORY)

		# Assert
		self.assertEqual(2, len(files))
		self.assertTrue('file.npy')

	def test_get_all_trial_files_no_files_success(self):
		# Arrange
		existing_files =  os.listdir(FILE_DIRECTORY)
		for file in existing_files:
			os.remove(f'{FILE_DIRECTORY}/{file}')

		# Act
		files = f.get_all_files(FILE_DIRECTORY)

		# Assert
		self.assertEqual(0, len(files))

if __name__ == "__main__":
	unittest.main()