import math as m 
import numpy as np
from utils import angle_calculation_utils as a

def get_statistics(trial_results, include_choice_stats):
    stats = calculate_default_stats(trial_results)
    if include_choice_stats:
        choice_stats = calculate_choice_stats(trial_results)
        stats.update(choiceStats)

    return stats 

def calculate_default_stats(trial_results):
    default_stats = get_empty_default_stats()

    predictions = trial_results['predictions']
    all_object_locations = trial_results['all_object_locations']
    flight_intervals = trial_results['flight_intervals']
    headings = trial_results['headings']
    length_video = trial_results['length_video']

    if predictions:
        total_flying_time = calculate_total_flying_time(flight_intervals)
        
        frames_identified = len(all_object_locations)
        total_frames = len(predictions)
        proportion_flying_time = total_flying_time / length_video

        if proportion_flying_time > 0:
            x, y = calculate_xy(headings)
            averageR = calculate_average_r(x, y)
            average_theta = calculate_average_theta(x, y)
        else:
            averageR = None 
            average_theta = None

        default_stats['length_video'] = length_video
        default_stats['total_frames'] = total_frames
        default_stats['frames_identified'] = frames_identified
        default_stats['total_flying_time'] = total_flying_time
        default_stats['proportion_flying_time'] = proportion_flying_time
        default_stats['average_r'] = averageR
        default_stats['average_theta'] = average_theta

    return default_stats 

def get_empty_default_stats():
    default_stats = {}
    default_stats.setdefault('length_video', "no predictions")
    default_stats.setdefault('total_frames', "< < < < < <")
    default_stats.setdefault('frames_identified', "< < < < < <")
    default_stats.setdefault('total_flying_time', "< < < < < <")
    default_stats.setdefault('proportion_flying_time', "< < < < < <")
    default_stats.setdefault('average_r', "< < < < < <")
    default_stats.setdefault('average_theta', "< < < < < <")
    return default_stats

def get_total_frames(predictions):
    return len([frame for frame in predictions.keys()])

def get_frames_identified(all_object_locations):
    return len([second for second in all_object_locations.keys()])

def calculate_total_flying_time(flight_intervals):
    total_flying_time = 0
    for flight_interval in flight_intervals:
        duration = flight_interval[1] - flight_interval[0]
        total_flying_time += duration

    return total_flying_time

def calculate_xy(headings):
    angles = [angle for angle in headings.values()]
    n = len(angles)
    if n > 0:
        sum_sine = sum([m.sin(m.radians(angle)) for angle in angles])
        sum_cos = sum([m.cos(m.radians(angle)) for angle in angles])
        y = sum_sine / n 
        x = sum_cos / n 

    return x, y

def calculate_average_r(x, y):
    return m.sqrt((x**2 + y**2))

def calculate_average_theta(x, y):
    average_theta = a.calculate_absolute_angle(x, y)
    quadrant = a.calculate_normal_quadrant(x, y)
    return a.correct_angle_based_on_quadrant(average_theta, quadrant)

def calculate_choice_stats(trial_results):
    predictions = trial_results['predictions']
    all_object_locations = trial_results['all_object_locations']
    flight_intervals = trial_results['flight_intervals']
    headings = trial_results['headings']
    direction_durations = trial_results['direction_durations']

    choice_stats = get_empty_choice_stats()
    if predictions:
        first_direction = find_first_direction(direction_durations)
        longest_consistent_direction = find_longest_consistent_direction(direction_durations)
        total_time_flying_toward, total_time_flying_away = calculate_total_flying_time_each_direction()
        
        thresholds = [num for num in range(1, 6)] + [10]
        for threshold in thresholds:
            first_consistent_direction = find_first_consistent_direction(direction_durations, threshold)
            choice_stats[f'first_consistent_direction.{threshold}'] = first_consistent_direction

        choice_stats['first_direction'] = first_direction
        choice_stats['longest_consistent_direction'] = longest_consistent_direction
        choice_stats['total_time_flying_toward'] = total_time_flying_toward
        choice_stats['total_time_flying_away'] = total_time_flying_away
        choice_stats['number_direction_switches'] = len(direction_durations['direction'])

    return choice_stats

def get_empty_choice_stats():
    choice_stats = {}
    choice_stats.setdefault('first_direction', "< < < < < <")
    choice_stats.setdefault('longest_consistent_direction', "< < < < < <")
    choice_stats.setdefault('total_time_flying_toward', "< < < < < <")
    choice_stats.setdefault('total_time_flying_away', "< < < < < <")
    choice_stats.setdefault('number_direction_switches', "< < < < < <")

    thresholds = [num for num in range(1, 6)] + [10]
    for threshold in thresholds:
        choice_stats.setdefault(f'first_consistent_direction.{threshold}', "< < < < < <")

    return choice_stats

def find_first_direction(direction_durations):
    first_direction = None
    directions = direction_durations['direction']
    if directions != []:
        first_direction = directions[0]

    return first_direction

def find_longest_consistent_direction(direction_durations):
    direction_max_duration = None
    directions = direction_durations['direction']
    durations = direction_durations['duration']

    if durations != []:
        max_duration = max(durations)
        max_duration_index = durations.index(max_duration)
        direction_max_duration = directions[max_duration_index]

    return direction_max_duration

def calculate_total_flying_time_each_direction(direction_durations):
    total_time_flying_toward = 0 
    total_time_flying_away = 0
    directions = direction_durations['direction']
    durations = direction_durations['duration']

    for i in range(len(directions)):
        direction = directions[i]
        duration = durations[i]

        if direction == 'toward':
            total_time_flying_toward += duration 
        else:
            total_time_flying_away += duration
            
    return [total_time_flying_toward, total_time_flying_away]

def find_first_consistent_direction(direction_durations, threshold):
    durations = np.array(direction_durations['duration'])
    directions = np.array(direction_durations['direction'])

    directions_thresholded = directions[durations >= threshold]
    if len(directions_thresholded) > 0:
        return directions_thresholded[0]
    else:
        return None
    

