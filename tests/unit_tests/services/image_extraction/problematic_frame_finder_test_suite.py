import sys
import unittest
import numpy as np

sys.path.append('../../')
from application.backend.components.problematic_frame_finder import ProblematicFrameFinder

# Function names must be in camel case to be recognized by the unittest library
class ProblematicFrameFinderTestSuite(unittest.TestCase):

	def setUp(self):
		prediction_file_directory = ''
		num_unique_objects = 0
		all_videos = []
		self.problematic_frame_finder = ProblematicFrameFinder(prediction_file_directory, num_unique_objects, all_videos)

	def runTest(self):
		self.testHasDuplicateObjects()
		self.testFindProblems()

	def testHasDuplicateObjects(self):
		labels = np.array([0, 1, 2])
		self.assertFalse(self.problematic_frame_finder.has_duplicate_objects(labels))

		labels = np.array([0, 1, 1])
		self.assertTrue(self.problematic_frame_finder.has_duplicate_objects(labels))

	def testFindProblems(self):
		self.problematic_frame_finder.num_unique_objects = 3
		predictions = {1: np.array([[0, 0, 0, 0, 0.9, 0], 
						   			[0, 0, 0, 0, 0.9, 1],
						   			[0, 0, 0, 0, 0.9, 2]])}
		self.assertEqual([[], []], self.problematic_frame_finder.find_problems(predictions))

		predictions = {1: np.array([[0, 0, 0, 0, 0.9, 0], 
						   			[0, 0, 0, 0, 0.9, 1],
						   			[0, 0, 0, 0, 0.9, 1],
						   			[0, 0, 0, 0, 0.9, 2]])}
		self.assertEqual([[1], []], self.problematic_frame_finder.find_problems(predictions))

		predictions = {1: np.array([[0, 0, 0, 0, 0.9, 0], 
						   			[0, 0, 0, 0, 0.9, 1]])}
		self.assertEqual([[], [1]], self.problematic_frame_finder.find_problems(predictions))

if __name__ == "__main__":
	unittest.main()