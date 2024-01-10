from utils.prediction_analysis import compass_utils as c 

'''
    Serial implementation is more efficient than parallelized implementation
    due to overhead that comes with creating processes
'''
class CompassFileService():

    def __init__(self, file_directory, compass_label_map):
        self.file_directory = file_directory
        self.compass_label_map = compass_label_map

    def process_compass_files(self, compass_files):
        north_angles = []
        for compass_file in compass_files:
            file_path = f'{self.file_directory}/{compass_file}'
            north_angle = c.get_north_angle(file_path, self.compass_label_map)

            if north_angle != None:
                north_angles.append([compass_file, north_angle])

        return north_angles
        

        

        