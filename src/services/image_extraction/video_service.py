import os
import cv2 
import random as r

''' 
    This class is reponsible for opening videos, getting video characteristics,
    and extracting frames.
'''
class VideoService():

    def __init__(self, video, num_frames_per_video, problematic_frames, file_directory, save_directory):
        self.video = video
        self.video_name = video[:-4]
        self.num_frames_per_video = num_frames_per_video
        self.problematic_frames = problematic_frames
        self.file_directory = file_directory
        self.save_directory = save_directory
        self.video_size = 0
        self.frame_probability = 0
        self.total_video_frames = 0

    def initialize(self):
        # This method is separated from the constructor to make
        # unit testing easier
        self.video_size = self.get_video_size()
        self.total_video_frames = self.get_total_video_frames()
        self.frame_probability = self.calculate_frame_probability()

    def get_video_size(self):
        return os.path.getsize(f'{self.file_directory}/{self.video}')

    def get_total_video_frames(self):
        try:
            return self.read_total_video_frames()
        except:
            return self.estimate_total_video_frames()

    def read_total_video_frames(self):
        return int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))

    def estimate_total_video_frames(self):
        SIZE_OF_FRAME = 18000
        return int(self.video_size / SIZE_OF_FRAME)

    def calculate_frame_probability(self):
        # If probability is too low, the app will take a long time extracting images
        threshold_probability = 0.05
        length_problematic_frames = len(self.problematic_frames)
        if length_problematic_frames > 0:
            threshold_probability = 0.9
            probability = self.num_frames_per_video / length_problematic_frames
        else:
            probability = self.num_frames_per_video / self.total_video_frames

        return probability if probability > threshold_probability else threshold_probability 

    def extract_and_save_frames(self):
        saved_num_frames = 0
        frame_num = 1
        opened_video = cv2.VideoCapture(f'{self.file_directory}/{self.video}')
        while opened_video.isOpened():
            reading_properly, frame = opened_video.read()
            if reading_properly:
                if self.frame_is_selected(frame_num):
                    resized_frame = cv2.resize(frame, None, fx=0.5, fy=0.5)
                    cv2.imwrite(f'{self.save_directory}/{self.video_name}_{frame_num}.jpg', resized_frame)
                    saved_num_frames += 1

            if saved_num_frames == self.num_frames_per_video:
                break

            frame_num += 1

        opened_video.release()
        cv2.destroyAllWindows()

    def frame_is_selected(self, frame_num, random_float=None):
        if not random_float:
            random_float = r.random()

        is_selected = False
        if self.problematic_frames:
            if frame_num in self.problematic_frames and random_float <= self.frame_probability:
                is_selected = True 
            else:
                is_selected = False
        else:
            if random_float <= self.frame_probability:
                is_selected = True
            else:
                is_selected = False
                
        return is_selected
