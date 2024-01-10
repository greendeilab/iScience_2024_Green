from PyQt5 import QtCore as qtc 
from .process import Process 
from services.compass_file_service import CompassFileService
from services.trial_file_service import TrialFileService
from utils import file_utils as f
import time 

'''
    This class coordinates the processing of trial data (in the form of .npy files). 
    Users have the option to calibrate the setup so the resulting monarch flight vector 
    is relative to north. Otherwise, users get the vectors as they appear in the videos.
'''
class PredictionAnalysisOrchestrator(Process):

    def __init__(self):
        super().__init__()
        self.file_directory = ''
        self.save_directory = ''
        self.calibrate_setup = False
        self.include_choice_stats = False
        self.duration_threshold = -1
        self.name_excel_file = ''
        self.one_file = False
        self.desired_video_length = 600

    def run(self):
        start_time = time.time()
        
        compass_label_map, trial_label_map = self.get_label_maps()
        self.total_tasks = 2 if self.calibrate_setup else 1

        trial_files, compass_files = f.get_prediction_files(self.file_directory, self.one_file)

        north_angles = []
        if self.calibrate_setup:
            self.next_step('\tProcessing compass files...')
            compass_file_service = CompassFileService(self.file_directory, compass_label_map)
            north_angles = compass_file_service.process_compass_files(compass_files)
            self.task_completed()

        self.next_step("\tProcessing trial files...")
        trial_file_service = TrialFileService(self.file_directory, 
                                              self.duration_threshold, 
                                              self.desired_video_length, 
                                              self.include_choice_stats, 
                                              trial_label_map, 
                                              north_angles)
        all_trial_statistics = trial_file_service.process_trial_files(trial_files)

        f.save_results(self.save_directory, all_trial_statistics, self.name_excel_file)
        self.task_completed()
        self.finished_process()

        end_time = time.time()
        elapsed_time = end_time - start_time

        print(f"Elapsed time: {elapsed_time} seconds")

    

    @qtc.pyqtSlot(dict)
    def receive_info(self, info):
        # Important info that is gathered from the view (obtained from emitWidgetInfo())
        self.file_directory = info['file_directory']
        self.save_directory = info['save_directory']
        self.calibrate_setup = info['calibrate_setup']
        self.include_choice_stats = info['include_choice_stats']
        self.duration_threshold = info['duration_threshold']
        self.name_excel_file = info['name_excel_file']

    def get_label_maps(self):
        ''' 
        These label maps are fed to Compass and Trial objects and they link the string-based labels
        we're interested in (such as north) with the integer-based labels the model uses. 
        
        ** You only need to change the values of the dictionaries (i.e. the numbers). The keys are used by 
            Compass and Trial so they should not be changed **    
        '''
        if self.one_file:
            label_map = {'origin': 0, 'north': 1, 'body': 2, 'head': 3}
            compass_label_map = label_map
            trial_label_map = label_map
        else:
            compass_label_map = {'origin': 0, 'north': 1}
            trial_label_map = {'head': 0, 'origin': 1, 'body': 2}

        return compass_label_map, trial_label_map

