from utils import angle_calculation_utils as a 
from utils import flight_interval_utils as f
from utils import direction_duration_utils as d
from utils import file_utils as fu
from utils import object_location_utils as o
import numpy as np
import math

IMPORTANT_LABELS = set(['body'])
    
def get_results(file_path, label_map, duration_threshold, north_angles, desired_video_length=None):
    results = get_empty_results()
    file = file_path.split('/')[-1]

    if desired_video_length is not None:
        predictions, length_video = fu.open_prediction_file_as_trial_and_trim(file_path, desired_video_length)
    else:
        predictions, length_video = fu.open_prediction_file_as_trial(file_path)

    all_object_locations = o.locate_all(predictions, label_map, IMPORTANT_LABELS)
    
    if all_object_locations:
        body_locations = o.filter_object_locations(all_object_locations, 'body')
        origin_locations = o.filter_object_locations(all_object_locations, 'origin')

        # we are choosing the middle location to filter out any extremes
        best_origin_location = o.get_middle_location(origin_locations)  
        if best_origin_location:
            flight_intervals = f.locate_all(body_locations, duration_threshold)
            headings = calculate_headings(all_object_locations, best_origin_location, flight_intervals, file, north_angles)
            direction_durations = d.find_direction_durations(headings, flight_intervals)

            results['predictions'] = predictions
            results['all_object_locations'] = all_object_locations
            results['flight_intervals'] = flight_intervals
            results['headings'] = headings
            results['direction_durations'] = direction_durations
            results['length_video'] = length_video
    
    return results

def get_empty_results():
    results = {}
    results.setdefault('predictions', None)
    results.setdefault('all_object_locations', None)
    results.setdefault('flight_intervals', None)
    results.setdefault('headings', None)
    results.setdefault('direction_durations', None)
    results.setdefault('length_video', None)
    return results

def calculate_headings(all_object_locations, best_origin_location, flight_intervals, file, north_angles):
    headings = {}
    for second, locations in all_object_locations.items():
        if f.is_during_flight_interval(second, flight_intervals):
            monarch_box = get_monarch_box(locations)
            if monarch_box:
                heading = calculate_heading(monarch_box, best_origin_location, file, north_angles)
                headings.setdefault(second, heading)

    return headings 

def get_monarch_box(locations):
    # If the head is present, use that to represent the location of the monarch otherwise use the body
    all_object_labels = list(locations.keys())
    if 'head' in all_object_labels and locations['head']:
        monarch_box = locations['head']
    elif 'body' in all_object_labels and locations['body']:
        monarch_box = locations['body']
    else:
        return None

    return monarch_box

def calculate_heading(monarch_box, best_origin_location, file, north_angles):
    heading = a.calculate(monarch_box, best_origin_location)
    if len(north_angles) > 0:
        corresponding_compass_file_index = get_corresponding_compass_file(file, north_angles)
        north_angle = north_angles[corresponding_compass_file_index][1]
        heading = calibrate_to_north_angle(north_angle, heading)

    return heading

def calibrate_to_north_angle(north_angle, heading):
    calibrated_angle = 90 - north_angle + heading
    if calibrated_angle > 360:
        calibrated_angle -= 360
    elif calibrated_angle < 0:
        calibrated_angle += 360

    return calibrated_angle

def get_corresponding_compass_file(file, north_angles):
    ''' 
    Finds the most appropriate compass file for calibration by searching for the 
    file that is closet in time.
    ''' 
    compass_files = [north_angle[0] for north_angle in north_angles]
    score = []

    for compass_file in compass_files:
        trial_day, trial_time = fu.get_file_attributes(file)
        compass_day, compass_time = fu.get_file_attributes(compass_file)
        
        if trial_day == compass_day:
            day_difference = abs(trial_day - compass_day) * 10**7
            time_difference = abs(trial_time - compass_time)
            total_difference = day_difference + time_difference
            score.append(total_difference)
        else:
            score.append(10**8)

    assert min(score) < 10**8, f"Corresponding compass file cannot be found for {file}"
    min_difference_index = score.index(min(score))

    return min_difference_index

    



