import sys
import unittest

sys.path.append('../../../src/')
from orchestrators.image_extraction import ImageExtractionOrchestrator

# Function names must be in camel case to be recognized by the unittest library
class ImageExtractionOrchestratorTestSuite(unittest.TestCase):

	def setUp(self):
		self.orchestrator = ImageExtractionOrchestrator()
		self.orchestrator.num_videos_to_process = 5

	def test_select_most_problematic_videos_duplicate_object_frames_only_success(self):
		# Arrange
		problematic_frame_info = {}
		problematic_frame_info['video.MOV'] = {'duplicate_object_frames': [], 'missing_object_frames': [3, 4, 5]}
		problematic_frame_info['video1.MOV'] = {'duplicate_object_frames': [0, 1, 2], 'missing_object_frames': [3, 4, 5]}
		problematic_frame_info['video2.MOV'] = {'duplicate_object_frames': [0, 1, 2, 3], 'missing_object_frames': []}
		
		self.orchestrator.find_duplicate_objects = True
		self.orchestrator.find_missing_objects = False

		expected_problematic_videos = ['video2.MOV', 'video1.MOV']

		# Act
		actual_problematic_videos = self.orchestrator.select_most_problematic_videos(problematic_frame_info)
		
		# Assert
		self.assertCountEqual(expected_problematic_videos, actual_problematic_videos)

	def test_select_most_problematic_videos_missing_object_frames_only_success(self):
		# Arrange
		problematic_frame_info = {}
		problematic_frame_info['video.MOV'] = {'duplicate_object_frames': [], 'missing_object_frames': [3, 4, 5]}
		problematic_frame_info['video1.MOV'] = {'duplicate_object_frames': [0, 1, 2], 'missing_object_frames': [3, 4, 5]}
		problematic_frame_info['video2.MOV'] = {'duplicate_object_frames': [0, 1, 2, 3], 'missing_object_frames': []}

		self.orchestrator.find_duplicate_objects = False
		self.orchestrator.find_missing_objects = True
		
		expected_problematic_videos = ['video.MOV', 'video1.MOV']

		# Act
		actual_problematic_videos = self.orchestrator.select_most_problematic_videos(problematic_frame_info)

		# Assert
		self.assertCountEqual(expected_problematic_videos, actual_problematic_videos)

	def test_select_most_problematic_videos_missing_objects_and_duplicate_frames_success(self):
		# Arrange
		problematic_frame_info = {}
		problematic_frame_info['video.MOV'] = {'duplicate_object_frames': [], 'missing_object_frames': [3, 4, 5]}
		problematic_frame_info['video1.MOV'] = {'duplicate_object_frames': [0, 1, 2], 'missing_object_frames': [3, 4, 5]}
		problematic_frame_info['video2.MOV'] = {'duplicate_object_frames': [0, 1, 2, 3], 'missing_object_frames': []}

		self.orchestrator.find_duplicate_objects = True
		self.orchestrator.find_missing_objects = True 

		expected_problematic_videos = ['video.MOV', 'video1.MOV', 'video2.MOV']

		# Act
		actual_problematic_videos = self.orchestrator.select_most_problematic_videos(problematic_frame_info)

		# Assert
		self.assertCountEqual(expected_problematic_videos, actual_problematic_videos)

	def test_select_most_problematic_videos_no_problematic_frames_success(self):
		# Arrange
		problematic_frame_info = {}

		# Act
		actual_problematic_videos = self.orchestrator.select_most_problematic_videos(problematic_frame_info)

		# Assert
		self.assertEqual([], actual_problematic_videos)

	def test_get_problematic_frames_success(self):
		# Arrange
		problematic_frame_info = {'video.mov': {'duplicate_object_frames': [0, 1, 2, 3, 4], 'missing_object_frames': [5, 6, 7, 8, 9]}}
		video = "video.mov"
		
		expected_problematic_frames = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
		self.orchestrator.find_missing_objects = True
		self.orchestrator.find_duplicate_objects = True

		# Act
		actual_problematic_frames = self.orchestrator.get_problematic_frames(video, problematic_frame_info)

		# Assert
		self.assertEqual(expected_problematic_frames, actual_problematic_frames)

	def test_get_problematic_frames_no_problems_success(self):
		# Arrange
		problematic_frame_info = {'video.mov': {'duplicate_object_frames': [0, 1, 2, 3, 4], 'missing_object_frames': [5, 6, 7, 8, 9]}}
		video = "video.mov"

		self.orchestrator.find_missing_objects = False
		self.orchestrator.find_duplicate_objects = False

		# Act
		actual_problematic_frames = self.orchestrator.get_problematic_frames(video, problematic_frame_info)

		# Assert
		self.assertEqual(set(), actual_problematic_frames)

	def test_get_equal_num_frames_success(self):
		# Arrange
		duplicate_object_frames = [1, 2, 3]
		missing_object_frames = [4, 5, 6, 7]

		# Act
		result = self.orchestrator.get_equal_num_frames(duplicate_object_frames, missing_object_frames)

		# Assert
		self.assertEqual(6, len(result[0] + result[1]))

	def test_get_equal_num_frames_success(self):
		# Arrange
		duplicate_object_frames = [1, 2, 3, 4]
		missing_object_frames = [5, 6, 7]

		# Act
		result = self.orchestrator.get_equal_num_frames(duplicate_object_frames, missing_object_frames)

		# Assert
		self.assertEqual(6, len(result[0] + result[1]))

if __name__ == "__main__":
	unittest.main()