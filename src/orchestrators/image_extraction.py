import os
import random as r
from PyQt5 import QtCore as qtc
from .process import Process
from utils.image_extraction import video_utils as v
from utils.image_extraction import problematic_frame_utils as p
from utils import file_utils as f 

'''
    This class coordinates the extraction of images from videos (.MOV) 
    to be used in model training. If problematic frames are to be extracted,
    it will use the most problematic videos to sample from. 
    Otherwise it will randomly select videos within the provided folder.
'''
class ImageExtractionOrchestrator(Process):

    def __init__(self):
        super().__init__()
        self.file_directory = ''
        self.save_directory = ''
        self.num_frames_per_video = 0
        self.num_videos_to_process = 0
        self.extract_problematic_frames = False
        self.find_duplicate_objects = False
        self.find_missing_objects = False
        self.prediction_file_directory = ''
        self.num_unique_objects = 0

    def run(self):
        all_videos = f.get_all_videos()
        self.total_tasks = self.num_videos_to_process if len(all_videos) >= self.num_videos_to_process else len(all_videos)
        type_frame = 'random'

        if self.extract_problematic_frames:
            type_frame = 'problematic'
            self.total_tasks += 2

            self.next_step("\tFinding problematic frames...")
            problematic_frame_info = p.locate_all(self.prediction_file_directory, self.num_unique_objects, all_videos)
            self.task_completed()       

            self.next_step("\tGetting videos...")
            videos_to_process = self.select_most_problematic_videos(problematic_frame_info)
            self.task_completed()
        else:     
            self.total_tasks += 1
            self.next_step("\tGetting videos...")
            videos_to_process = self.select_random_videos(all_videos)
            self.task_completed()

        self.next_step(f"\tExtracting {type_frame} frames...")
        for video in videos_to_process:
            problematic_frames = self.get_problematic_frames(video) if self.extract_problematic_frames else []
            video.extract_and_save(self.file_directory, self.save_directory, video, self.num_frames_per_video, problematic_frames)
            self.task_completed()

        self.finished_process()

    def select_most_problematic_videos(self, problematic_frame_info):
        '''
            Videos are given a score which indicates the number of problematic 
            frames they contain. The videos with the highest score are selected.
        '''
        most_problematic_videos = []
        scores = []
        for video, problems in problematic_frame_info.items():
            score = 0

            num_duplicate_object_frames = len(problems['duplicate_object_frames'])
            num_missing_object_frames = len(problems['missing_object_frames'])

            if self.find_duplicate_objects:
                score += num_duplicate_object_frames
            if self.find_missing_objects:
                score += num_missing_object_frames
            scores.append((video, score))

        scores = sorted(scores, key=lambda x: x[1], reverse=True)     
        for video, score in scores:
            if len(most_problematic_videos) < self.num_videos_to_process and score > 0:
                most_problematic_videos.append(video)
            elif len(most_problematic_videos) == self.num_videos_to_process:
                break

        return most_problematic_videos

    def select_random_videos(self, all_videos):
        if len(all_videos) <= self.num_videos_to_process: return all_videos

        random_videos = []
        i = 0
        for video in all_videos:
            num_random_videos = len(random_videos)
            num_remaining_videos = len(all_videos) - i
            num_remaining_videos_to_select = self.num_videos_to_process - num_random_videos
            selection_probability = num_remaining_videos_to_select / num_remaining_videos

            if num_random_videos == self.num_videos_to_process:
                break
            elif self.video_is_selected(selection_probability):
                random_videos.append(video)
            i += 1

        return random_videos

    def video_is_selected(self, selection_probability):
        random_float = r.random()
        if random_float <= selection_probability:
            return True 
        else:   
            return False

    def get_problematic_frames(self, video, problematic_frame_info):
        problematic_frames = []
        duplicate_object_frames = problematic_frame_info[video]['duplicate_object_frames']
        missing_object_frames = problematic_frame_info[video]['missing_object_frames']

        # If the user wants images with missing objects and duplicate objects,
        # ensure that the number of instances for each problem is equal to prevent training bias
        if self.find_missing_objects and self.find_duplicate_objects:
            if len(duplicate_object_frames) != len(missing_object_frames):
                duplicate_object_frames, missing_object_frames = self.get_equal_num_frames(duplicate_object_frames, missing_object_frames)
            problematic_frames += duplicate_object_frames + missing_object_frames
        elif self.find_missing_objects and not self.find_duplicate_objects:
            problematic_frames = missing_object_frames
        elif not self.find_missing_objects and self.find_duplicate_objects:
            problematic_frames = duplicate_object_frames

        return set(problematic_frames)

    def get_equal_num_frames(self, duplicate_object_frames, missing_object_frames):
        duplicate_object_frames_resized = []
        missing_object_frames_resized = []

        # Determine which set of frames is the smallest in size and take 
        # the same number of frames from the other set
        if len(duplicate_object_frames) > len(missing_object_frames):
            missing_object_frames_resized = missing_object_frames
            limiting_array = missing_object_frames
            limiting_size = len(missing_object_frames)
            array_to_populate = duplicate_object_frames_resized
            array_to_choose_from = duplicate_object_frames
        else:
            duplicate_object_frames_resized = duplicate_object_frames
            limiting_array = duplicate_object_frames
            limiting_size = len(duplicate_object_frames)
            array_to_populate = missing_object_frames_resized
            array_to_choose_from = missing_object_frames

        # First choose the frames that appear in both sets
        for frame_num in limiting_array:
            if frame_num in array_to_choose_from:
                array_to_populate.append(frame_num)
                array_to_choose_from.remove(frame_num)

        # Randomly select the remaining frames
        num_remaining_frames_to_choose = limiting_size - len(array_to_populate)
        for __ in range(num_remaining_frames_to_choose):
            choice = r.choice(array_to_choose_from)
            array_to_populate.append(choice)
            array_to_choose_from.remove(choice)

        return [duplicate_object_frames_resized, missing_object_frames_resized]

    @qtc.pyqtSlot(dict)
    def receive_info(self, info):
        # Important info that is gathered from the view (obtained from emitWidgetInfo())
        self.file_directory = info['file_directory']
        self.save_directory = info['save_directory']
        self.num_frames_per_video = info['num_frames_per_video']
        self.num_videos_to_process = info['num_videos_to_process']
        self.extract_problematic_frames = info['extract_problematic_frames']
        self.find_duplicate_objects = info['find_duplicate_objects']
        self.find_missing_objects = info['find_missing_objects']
        self.prediction_file_directory = info['prediction_file_directory']
        self.num_unique_objects = info['num_unique_objects']
