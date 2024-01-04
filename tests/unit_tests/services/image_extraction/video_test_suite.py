import sys
import unittest

sys.path.append('../../')
from application.backend.components.video import Video

# Function names must be in camel case to be recognized by the unittest library
class VideoTestSuite(unittest.TestCase):

	def setUp(self):
		video = ''
		num_frames_per_video = 20
		problematic_frames = []
		file_directory = ''
		save_directory = ''
		self.video = Video(video, num_frames_per_video, problematic_frames, file_directory, save_directory)

	def runTest(self):
		self.testFrameIsSelected()
		
	def testFrameIsSelected(self):
		self.video.frame_probability = 0.5
		self.assertTrue(self.video.frame_is_selected(1, random_float=0.2))

		self.assertFalse(self.video.frame_is_selected(1, random_float=0.9))

		self.video.problematic_frames = [1, 2, 3, 4, 5]
		self.assertTrue(self.video.frame_is_selected(1, random_float=0.2))
		self.assertFalse(self.video.frame_is_selected(1, random_float=0.9))
		self.assertFalse(self.video.frame_is_selected(8, random_float=0.2))

if __name__ == "__main__":
	unittest.main()