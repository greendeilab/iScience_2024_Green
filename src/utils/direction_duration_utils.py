from utils import flight_interval_utils as f 

def find_direction_durations(headings, flight_intervals):
    reference_intervals = create_reference_intervals()
    direction_durations = {'duration': [], 'direction': []}
    seconds = [second for second in headings.keys()]
    angles = [angle for angle in headings.values()]

    duration_toward_ref = 0 
    duration_away_ref = 0
    for i in range(len(seconds)):
        if i == len(seconds) - 1:
            if duration_toward_ref > 0:
                direction_durations['direction'].append('toward')
                direction_durations['duration'].append(duration_toward_ref)
                duration_toward_ref = 0
            elif duration_away_ref > 0:
                direction_durations['direction'].append('away')
                direction_durations['duration'].append(duration_away_ref)
                duration_away_ref = 0
            break

        second = seconds[i]
        next_second = seconds[i + 1]
        angle = angles[i]
        if f.is_during_flight_interval(second, flight_intervals) and not f.is_end_of_flight_interval(second, flight_intervals):
            if is_flying_towards_reference(angle, reference_intervals):
                duration_toward_ref +=  next_second - second

                # If the individual was flying away from the reference, record it
                if duration_away_ref > 0:
                    direction_durations['direction'].append('away')
                    direction_durations['duration'].append(duration_away_ref)
                    duration_away_ref = 0
            else:
                duration_away_ref += next_second - second

                # If the individual was flying towards the reference, record it
                if duration_toward_ref > 0:
                    direction_durations['direction'].append('toward')
                    direction_durations['duration'].append(duration_toward_ref)
                    duration_toward_ref = 0

    return direction_durations

def create_reference_intervals(reference_angle=90, deviation=90):
    reference_intervals = []

    lower_bound = reference_angle - deviation
    upper_bound = reference_angle + deviation
    if lower_bound < 0:
        reference_intervals.append([360 + lower_bound, 360])
        reference_intervals.append([0, upper_bound])
    elif upper_bound > 360:
        reference_intervals.append([0, upper_bound - 360])
        reference_intervals.append([lower_bound, 360])
    else:
        reference_intervals.append([lower_bound, upper_bound])

    return reference_intervals

def is_flying_towards_reference(angle, reference_intervals):
    is_flying_towards_reference = False 
    for interval in reference_intervals:
        if angle >= interval[0] and angle < interval[1]:
            is_flying_towards_reference = True 

    return is_flying_towards_reference