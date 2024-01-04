import sys
import unittest

sys.path.append('../../')
from application.backend.image_extractor import ImageExtractor

# Function names must be in camel case to be recognized by the unittest library
class ImageExtractorTestSuite(unittest.TestCase):

	def setUp(self):
		self.image_extractor = ImageExtractor()
		self.image_extractor.find_duplicate_objects = True
		self.image_extractor.find_missing_objects = True
		self.image_extractor.num_videos_to_process = 5

	def runTest(self):
		self.testSelectMostProblematicVideos()

		self.setUp()
		self.testGetEqualNumFrames()

		self.setUp()
		self.testGetProblematicFrames()

	def testSelectMostProblematicVideos(self):
		self.image_extractor.problematic_frame_info = {'video.MOV': {'duplicate_object_frames': [], 
															  		'missing_object_frames': []},
		 											   'video1.MOV': {'duplicate_object_frames': [0, 1, 2], 
		 													   		'missing_object_frames': [3, 4, 5]},
		 											   'video2.MOV': {'duplicate_object_frames': [0, 1, 2, 3],
											   		'missing_object_frames': []}}
		
		self.image_extractor.find_missing_objects = False
		all_videos = ['video1.MOV', 'video2.MOV']
		self.assertEqual(['video2.MOV', 'video1.MOV'], self.image_extractor.select_most_problematic_videos())

		self.image_extractor.find_missing_objects = True
		self.image_extractor.find_duplicate_objects = False
		self.assertEqual(['video1.MOV'], self.image_extractor.select_most_problematic_videos())

		self.image_extractor.problematic_frame_info = {}
		self.assertEqual([], self.image_extractor.select_most_problematic_videos())

	def testGetEqualNumFrames(self):
		duplicate_object_frames = [1, 2, 3]
		missing_object_frames = [4, 5, 6, 7]
		result = self.image_extractor.get_equal_num_frames(duplicate_object_frames, missing_object_frames)
		self.assertEqual(6, len(result[0] + result[1]))

		duplicate_object_frames = [1, 2, 3, 4]
		missing_object_frames = [5, 6, 7]
		result = self.image_extractor.get_equal_num_frames(duplicate_object_frames, missing_object_frames)
		self.assertEqual(6, len(result[0] + result[1]))

		duplicate_object_frames = [1, 2, 3, 4, 5, 6, 7]
		missing_object_frames = [1, 2, 3]
		result = self.image_extractor.get_equal_num_frames(duplicate_object_frames, missing_object_frames)
		self.assertEqual([[1, 2, 3], [1, 2, 3]], result)

		duplicate_object_frames = [1, 2, 3]
		missing_object_frames = [1, 2, 3, 4, 5, 6, 7]
		result = self.image_extractor.get_equal_num_frames(duplicate_object_frames, missing_object_frames)
		self.assertEqual([[1, 2, 3], [1, 2, 3]], result)

		duplicate_object_frames = [1, 2, 3, 8]
		missing_object_frames = [1, 2, 4, 5, 6, 7]
		result = self.image_extractor.get_equal_num_frames(duplicate_object_frames, missing_object_frames)
		self.assertEqual(8, len(result[0] + result[1]))

	def testGetProblematicFrames(self):
		self.image_extractor.problematic_frame_info = {'video.mov': {'duplicate_object_frames': [0, 1, 2, 3, 4], 
															  'missing_object_frames': [5, 6, 7, 8, 9]}}
		video = "video.mov"
		self.assertEqual({0, 1, 2, 3, 4, 5, 6, 7, 8, 9}, self.image_extractor.get_problematic_frames(video))

		self.image_extractor.find_missing_objects = False
		self.image_extractor.find_duplicate_objects = False
		self.assertEqual(set(), self.image_extractor.get_problematic_frames(video))

if __name__ == "__main__":
	unittest.main()