import numpy as np 
from utils import file_utils as f 
from utils import object_location_utils as o

def locate_all(file_directory, num_unique_objects, all_videos):
	problematic_frame_info = {}
	prediction_files = f.get_all_files(file_directory)

	for file in prediction_files:
		file_name = f"{'_'.join(file.split('_')[:-f.NUM_TRAILING_FILE_PARAMS_TO_IGNORE])}"
		video = get_corresponding_video(file_name, all_videos)

		if video:
			problematic_frame_info.setdefault(video, {})
			predictions = f.open_prediction_file(f'{file_directory}/{file}');
			duplicate_object_frames, missing_object_frames = find_problems(predictions, num_unique_objects)
			problematic_frame_info[video].setdefault('duplicate_object_frames', duplicate_object_frames)
			problematic_frame_info[video].setdefault('missing_object_frames', missing_object_frames)

	return problematic_frame_info

def get_corresponding_video(file_name, all_videos):
	for video in all_videos:
		if file_name in video:
			return video

	return None

def find_problems(predictions, num_unique_objects):
	duplicate_object_frames = []
	missing_object_frames = []
	for frame_num, prediction_info in predictions.items():
		boxes, scores, labels = o.separate_prediction_info(prediction_info)
		labels = np.array(labels)
		num_unique_labels = np.unique(labels).shape[0]

		if num_unique_labels < num_unique_objects:
			missing_object_frames.append(frame_num)

		if has_duplicate_objects(labels):
			duplicate_object_frames.append(frame_num)

	return [duplicate_object_frames, missing_object_frames]

def has_duplicate_objects(labels):
	unique_labels = np.unique(labels)
	for label in unique_labels:
		if len(labels[labels == label]) > 1:
			return True
			
	return False





