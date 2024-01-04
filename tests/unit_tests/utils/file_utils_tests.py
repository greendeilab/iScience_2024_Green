import sys
import unittest
import os
import openpyxl as op 
import numpy as np

sys.path.append('../../../src')
from utils import file_utils as f

class FileUtilsTests(unittest.TestCase):

	def setUp(self):
		self.root_dir = '../files'
		self.wb = op.Workbook()
		self.empty_sheet = self.wb.active
	
	def test_is_compass_file_false(self):
		# Act
		is_compass_file = f.is_compass_file("compas.npy")

		# Assert
		self.assertFalse(is_compass_file)

	def test_is_compass_file_true(self):
		# Act
		is_compass_file = f.is_compass_file("compass_file.npy")

		# Assert
		self.assertTrue(is_compass_file)

	def test_get_file_attributes_success(self):
		# Arrange
		file = "20220914_102455_compass_predictions_yolo"

		# Act
		[date, time] = f.get_file_attributes(file);

		# Assert
		self.assertEqual(20220914, date)
		self.assertEqual(102455, time)

	def test_change_to_dot_notation_success(self):
		# Arrange
		attribute_names = ["stat_name", "stat", "statname", "long_stat_name"]
		expected_attribute_names = ["stat.name", "stat", "statname", "long.stat.name"]

		# Act
		actual_attribute_names = [f.change_to_dot_notation(attribute_name) for attribute_name in attribute_names]

		# Assert
		for i in range(len(actual_attribute_names)):
			self.assertEqual(expected_attribute_names[i], actual_attribute_names[i])

	def test_get_num_extra_headings_success(self):
		# Arrange
		file = "Date_time_predictions_yolo.npy"

		# Act
		num_extra_headings = f.get_num_extra_headings(file)

		# Assert
		self.assertEqual(2, num_extra_headings)

	def test_add_empty_headings_zero_success(self):
		# Arrange
		headings = ["heading1", "heading2"]
		expected_headings = headings

		# Act
		actual_headings = f.add_empty_headings(headings, 0)

		# Assert
		self.assertEqual(expected_headings, actual_headings)

	def test_add_empty_headings_1_success(self):
		# Arrange
		headings = ["heading1", "heading2"]
		expected_headings = ['heading1', '', 'heading2']

		# Act
		actual_headings = f.add_empty_headings(headings, 1)

		# Assert
		self.assertEqual(expected_headings, actual_headings)

	def test_create_headings_success(self):
		# Arrange
		trial_statistics = [['DATE_TIME_P1_predictions_yolo.npy', {'stat_name': 0, 'long_stat_name': 0, 'stat_stat': 0}]]
		expected_headings = ['file','', '', '', 'stat.name', 'long.stat.name', 'stat.stat']

		# Act
		actual_headings = f.create_headings(trial_statistics)

		# Assert
		self.assertEqual(expected_headings, actual_headings)

	def test_write_headings_to_sheet_success(self):
		# Arrange
		headings = ['col1_header', '', 'col3_header']
		sheet = self.wb.copy_worksheet(self.empty_sheet)

		col_letters = ['A', 'B', 'C']
		expected_sheet = self.wb.copy_worksheet(self.empty_sheet)
		for i in range(len(col_letters)):
			cell = f'{col_letters[i]}1'
			expected_sheet[cell] = headings[i]

		# Act
		actual_sheet = f.write_headings_to_sheet(headings, sheet, 'C')

		# Assert
		for i in range(len(col_letters)):
			cell = f'{col_letters[i]}1'
			self.assertEqual(expected_sheet[cell].value, actual_sheet[cell].value)

	def test_write_data_to_sheet_success(self):
		# Arrange
		trial_statistics = [
			['DATE_TIME_P1_predictions_yolo.npy', {'stat_name': 0, 'long_stat_name': 0, 'stat_stat': 0}],
			['DATE_TIME_predictions_yolo2.npy', {'stat_name': 0, 'long_stat_name': 0, 'stat_stat': 0}],
			['DATE_TIME_p2_p3_predictions_yolo3', {'stat_name': 0, 'long_stat_name': 0, 'stat_stat': 0}]
		]
		
		expected_rows = [
			['DATE_TIME_P1_predictions_yolo.npy', 'DATE', 'TIME', 'P1', None, 0, 0, 0],
			['DATE_TIME_predictions_yolo2.npy', 'DATE', 'TIME', None, None, 0, 0, 0],
			['DATE_TIME_p2_p3_predictions_yolo3', 'DATE', 'TIME', 'p2', 'p3', 0, 0, 0]
		]

		# Act
		actual_sheet = f.write_data_to_sheet(trial_statistics, self.empty_sheet, 'H')

		# Assert
		for i in range(len(expected_rows)):
			corresponding_row = 2 + i
			actual_row = self.extract_row_x_values(actual_sheet, corresponding_row, 'H')
			self.assertEqual(expected_rows[i], actual_row)

	def extract_row_x_values(self, sheet, row_num, max_col_letter):
		row_values = []
		for row in sheet[f'A{row_num}': f'{max_col_letter}{row_num}']:
			for cell in row:
				row_values.append(cell.value)

		return row_values

	def test_get_col_index_less_than_col_Z_success(self):
		# Act
		col_index = f.get_col_index('A1')

		# Assert
		self.assertEqual(1, col_index)

	def test_get_col_index_greater_than_col_Z_success(self):
		# Act
		col_index = f.get_col_index('AA1')

		# Assert
		self.assertEqual(27, col_index)

if __name__ == "__main__":
	unittest.main()