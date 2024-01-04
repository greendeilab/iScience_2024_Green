from multiprocessing import Pool 
from utils import trial_utils as t 
from utils import statistics_utils as s

class TrialFileService():

    def __init__(self, file_directory, duration_threshold, desired_video_length, include_choice_stats, trial_label_map, north_angles):
        self.file_directory = file_directory
        self.duration_threshold = duration_threshold
        self.desired_video_length = desired_video_length
        self.include_choice_stats = include_choice_stats
        self.trial_label_map = trial_label_map
        self.north_angles = north_angles

    def process_trial_files(self, trial_files):
        with Pool() as pool:
            all_trial_stats_list = pool.map(self.process, trial_files)

        return all_trial_stats_list

    def process(self, trial_file):
        file_path = f'{self.file_directory}/{trial_file}'
        trial_results = t.get_results(file_path, self.trial_label_map, self.duration_threshold, self.north_angles, self.desired_video_length)
        trial_statistics = s.get_statistics(trial_results, self.include_choice_stats)
        return [trial_file, trial_statistics]