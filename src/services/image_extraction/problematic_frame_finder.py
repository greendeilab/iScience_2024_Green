
import numpy as np 
from utils.file_handler import FileHandler
from utils.object_location_finder import ObjectLocationFinder 

class ProblematicFrameFinder():

	def __init__(self, prediction_file_directory, num_unique_objects, all_videos):
		self.prediction_file_directory = prediction_file_directory
		self.num_unique_objects = num_unique_objects
		self.all_videos = all_videos
		self.file_handler = FileHandler(prediction_file_directory)
		self.NUM_TRAILING_FILE_PARAMS_TO_IGNORE = self.file_handler.NUM_TRAILING_FILE_PARAMS_TO_IGNORE
		self.object_location_finder = ObjectLocationFinder({}, {}, ())

	def locate_all(self):
		problematic_frame_info = {}
		prediction_files = self.file_handler.get_all_files()
		for file in prediction_files:
			file_name = f"{'_'.join(file.split('_')[:-self.NUM_TRAILING_FILE_PARAMS_TO_IGNORE])}"
			video = self.get_corresponding_video(file_name)
			if video:
				problematic_frame_info.setdefault(video, {})
				predictions = self.file_handler.get_predictions(file)
				duplicate_object_frames, missing_object_frames = self.find_problems(predictions)
				problematic_frame_info[video].setdefault('duplicate_object_frames', duplicate_object_frames)
				problematic_frame_info[video].setdefault('missing_object_frames', missing_object_frames)

		return problematic_frame_info

	def get_corresponding_video(self, file_name):
		for video in self.all_videos:
			if file_name in video:
				return video

		return None

	def find_problems(self, predictions):
		duplicate_object_frames = []
		missing_object_frames = []
		for frame_num, prediction_info in predictions.items():
			boxes, scores, labels = self.object_location_finder.separate_prediction_info(prediction_info)
			labels = np.array(labels)
			num_unique_labels = np.unique(labels).shape[0]
	
			if num_unique_labels < self.num_unique_objects:
				missing_object_frames.append(frame_num)

			if self.has_duplicate_objects(labels):
				duplicate_object_frames.append(frame_num)

		return [duplicate_object_frames, missing_object_frames]

	def has_duplicate_objects(self, labels):
		has_duplicate_objects = False
		unique_labels = np.unique(labels)
		for label in unique_labels:
			if len(labels[labels == label]) > 1:
				has_duplicate_objects = True
				break
				
		return has_duplicate_objects





