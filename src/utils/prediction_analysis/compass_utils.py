import numpy as np
import statistics as s
from utils import object_location_utils as o
from utils.prediction_analysis import angle_calculation_utils as a
from utils import file_utils as f 

IMPORTANT_LABELS = set(['origin', 'north'])

def get_north_angle(file_path, label_map):
    # taking the median of all north angles will filter out extreme / wrong values 
    # (if the model incorrectly identifies the origin or north needle)
    try:
        predictions = f.open_prediction_file(file_path)
        north_angles = calculate_north_angles(predictions, label_map) 
        best_north_angle = s.median(north_angles)
    except s.StatisticsError:
        best_north_angle = None
    
    return best_north_angle

def calculate_north_angles(predictions, label_map):
    north_angles = [] 
    
    all_object_locations = o.locate_all(predictions, label_map, IMPORTANT_LABELS)
    for locations in all_object_locations.values():
        north_box = locations['north']
        origin_box = locations['origin']
        if north_box != [] and origin_box != []:
            angle = a.calculate(north_box, origin_box)
            north_angles.append(angle)

    return north_angles

    
    