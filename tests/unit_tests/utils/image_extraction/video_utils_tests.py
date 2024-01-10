import sys
import unittest

sys.path.append('../../../../src')
from utils.image_extraction import video_utils as v

class VideoUtilsTests(unittest.TestCase):

	def test_calculate_frame_extraction_probability_problematic_frames_success(self):
		# Arrange
		problematic_frames = [1, 2, 3, 4]
		num_frames_per_video = 4
		total_frames = 10

		# Act
		frame_extraction_probability = v.calculate_frame_extraction_probability(problematic_frames, num_frames_per_video, total_frames)

		# Assert
		self.assertEqual(1, frame_extraction_probability)

	def test_calculate_frame_extraction_probability_no_problematic_frames_success(self):
		# Arrange
		problematic_frames = []
		num_frames_per_video = 4
		total_frames = 10

		# Act
		frame_extraction_probability = v.calculate_frame_extraction_probability(problematic_frames, num_frames_per_video, total_frames)

		# Assert
		self.assertEqual(0.4, frame_extraction_probability)

	def test_calculate_frame_probability_below_threshold_success(self):
		# Arrange
		problematic_frames = []
		num_frames_per_video = 4
		total_frames = 10000

		# Act
		frame_extraction_probability = v.calculate_frame_extraction_probability(problematic_frames, num_frames_per_video, total_frames)

		# Assert
		self.assertEqual(0.05, frame_extraction_probability)

	def test_frame_is_selected_problematic_frame_true(self):
		# Arrange
		frame_num = 1
		problematic_frames = [1, 2, 3, 6]
		frame_extraction_probability = 0.5
		random_float = 0.2

		# Act
		frame_is_selected = v.frame_is_selected(frame_num, frame_extraction_probability, problematic_frames, random_float)

		# Assert
		self.assertTrue(frame_is_selected)

	def test_frame_is_selected_problematic_frame_false(self):
		# Arrange
		frame_num = 1
		problematic_frames = [1, 2, 3, 6]
		frame_extraction_probability = 0.5
		random_float = 0.75

		# Act
		frame_is_selected = v.frame_is_selected(frame_num, frame_extraction_probability, problematic_frames, random_float)

		# Assert
		self.assertFalse(frame_is_selected)

	def test_frame_is_selected_not_problematic_frame_true(self):
		# Arrange
		frame_num = 1
		problematic_frames = []
		frame_extraction_probability = 0.5
		random_float = 0.2

		# Act
		frame_is_selected = v.frame_is_selected(frame_num, frame_extraction_probability, problematic_frames, random_float)

		# Assert
		self.assertTrue(frame_is_selected)

	def test_frame_is_selected_not_problematic_frame_false(self):
		# Arrange
		frame_num = 1
		problematic_frames = []
		frame_extraction_probability = 0.5
		random_float = 0.75

		# Act
		frame_is_selected = v.frame_is_selected(frame_num, frame_extraction_probability, problematic_frames, random_float)

		# Assert
		self.assertFalse(frame_is_selected)

if __name__ == "__main__":
	unittest.main()