import sys
import unittest
import numpy as np

sys.path.append('../../../src')
from utils import object_location_utils as o

class ObjectLocationUtilsTests(unittest.TestCase):

	def test_find_object_locations_all_found_success(self):
		# Arrange
		prediction_info = np.array([[1, 2, 3, 4, 0.9, 0],
								   [5, 6, 7, 8, 0.9, 1],
								   [9, 10, 11, 12, 0.9, 2]])
		mapping = {'head': 0, 'origin': 1, 'body': 2}
		important_labels = set(['body'])

		expected_object_locations = {
			"head": [1, 2, 3, 4],
			"origin": [5, 6, 7, 8],
			"body": [9, 10, 11, 12]
		}

		# Act
		object_locations = o.find_object_locations(prediction_info, mapping, important_labels)

		# Assert
		self.assertEqual(expected_object_locations, object_locations)

	def test_find_object_locations_missing_important_object_none(self):
		# Arrange
		prediction_info = np.array([[1, 2, 3, 4, 0.9, 0],
								   [5, 6, 7, 8, 0.9, 1]])
		mapping = {'head': 0, 'origin': 1, 'body': 2}
		important_labels = set(['body'])

		# Act
		object_locations = o.find_object_locations(prediction_info, mapping, important_labels)

		# Assert
		self.assertIsNone(object_locations)


	def test_separate_prediction_info_success(self):
		# Arrange
		prediction_info = np.array([[1, 2, 3, 4, 0.9, 0],
								   [5, 6, 7, 8, 0.9, 1],
								   [9, 10, 11, 12, 0.9, 2]])

		expected_boxes = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
		expected_scores = [0.9, 0.9, 0.9]
		expected_labels = [0, 1, 2]

		# Act
		boxes, scores, labels = o.separate_prediction_info(prediction_info)

		# Assert
		self.assertEqual(expected_boxes, boxes)
		self.assertEqual(expected_scores, scores)
		self.assertEqual(expected_labels, labels)

	def test_filter_predictions_missing_label_success(self):
		# Arrange
		boxes = [[0], [1], [2]]
		scores = [0.95, 0.95, 0.95]
		labels = [0, 1, 1]
		mapping = {'head': 0, 'origin': 1, 'body': 2}

		expected_boxes = [[0], [1]]
		expected_labels = [0, 1]

		# Act
		[best_boxes, best_labels] = o.filter_predictions(mapping, boxes, scores, labels)

		# Assert
		self.assertEqual(expected_boxes, best_boxes)
		self.assertEqual(expected_labels, best_labels)

	def test_filter_predictions_no_duplicates_success(self):
		# Arrange
		boxes = [[0], [1], [2]]
		scores = [0.95, 0.95, 0.95]
		labels = [0, 1, 2]
		mapping = {'head': 0, 'origin': 1, 'body': 2}

		# Act
		[best_boxes, best_labels] = o.filter_predictions(mapping, boxes, scores, labels)

		self.assertEqual(boxes, best_boxes)
		self.assertEqual(labels, best_labels)

	def test_filter_predictions_duplicates_success(self):
		# Arrange
		boxes = [[0], [1], [2], [3]]
		scores = [0.95, 0.95, 0.95, 0.3]
		labels = [0, 1, 2, 2]
		mapping = {'head': 0, 'origin': 1, 'body': 2}

		expected_boxes = [[0], [1], [2]]
		expected_labels = [0, 1, 2]

		# Act
		[best_boxes, best_labels] = o.filter_predictions(mapping, boxes, scores, labels)
		
		# Assert
		self.assertEqual(expected_boxes, best_boxes)
		self.assertEqual(expected_labels, best_labels)
	
	def test_find_best_box_success(self):
		# Arrange
		boxes = [[0], [1], [2], [4], [5]]
		scores = [0.5, 0.8, 0.1, 0.9, 0.4]
		labels = np.array([1, 2, 2, 3, 3])

		# Act
		best_box = o.find_best_box(boxes, scores, labels, 2)

		# Assert
		self.assertEqual(boxes[1], best_box)

	def test_get_middle_location_boxes_present_success(self):
		# Arrange
		locations = {0: [0, 10], 1: [1, 9], 2: [], 3: [3, 7], 4: [4, 6], 5:[5, 5]}

		# Act
		middle_location = o.get_middle_location(locations)

		# Assert
		self.assertEqual(locations[3], middle_location)

	def test_get_middle_location_boxes_not_present_none(self):
		# Arrange
		locations = {0: [], 1: [], 2: [], 3: [], 4: [], 5:[]}

		# Act
		middle_location = o.get_middle_location(locations)

		# Assert
		self.assertIsNone(middle_location)

	def test_filter_object_locations_success(self):
		# Arrange
		all_object_locations = {0: {"head": [0], "body": [1]}, 1: {"head": [2], "body": [3]}}
		expected_object_locations = {0: [0], 1: [2]}

		# Act
		actual_object_locations = o.filter_object_locations(all_object_locations, "head")

		# Assert
		self.assertEqual(expected_object_locations, actual_object_locations)

if __name__ == "__main__":
	unittest.main()