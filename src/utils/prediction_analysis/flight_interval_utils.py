from utils import general_algorithms as g

# The minimum number of claps an indivdual needs to have within a second
# to be determined as flight
SECOND_THRESHOLD = 1
CLAP_THRESHOLD = 5 * SECOND_THRESHOLD

# The number of steps to the left and right of a point to determine if its a local min
STEPS_TO_THE_LEFT = -5
STEPS_TO_THE_RIGHT = 6

# Arbitrary threshold for determining if an individual is flying
FLUCTUATION_THRESHOLD = 20000

FUNC = lambda flight_interval, target: compare_with_tuple(flight_interval, target, 1)

def locate_all(body_locations, duration_threshold):
    seconds = [second for second, body_box in body_locations.items()]
    body_boxes = [body_box for body_box in body_locations.values()]

    body_areas = calculate_body_areas(body_boxes)
    body_fluctuations = calculate_body_fluctuations(seconds, body_areas)
    time_of_claps = find_time_of_claps(seconds, body_areas, body_fluctuations)
    flight_intervals = find_flight_intervals(time_of_claps)

    return filter_flight_intervals(flight_intervals, duration_threshold)

def calculate_body_areas(body_boxes):
    body_areas = []
    for body_box in body_boxes:
        body_areas.append(calculate_area(body_box))

    return body_areas

def calculate_area(box):
    XMIN, YMIN, XMAX, YMAX = 0, 1, 2, 3
    return (box[XMAX] - box[XMIN]) * (box[YMAX] - box[YMIN])

def calculate_body_fluctuations(seconds, body_areas):
    body_fluctuations = []
    for i in range(len(seconds) - 1):
        body_difference = body_areas[i + 1] - body_areas[i]
        time_difference = seconds[i + 1] - seconds[i]
        fluctuation = body_difference / time_difference
        body_fluctuations.append(fluctuation)

    return body_fluctuations 

def find_time_of_claps(seconds, body_areas, body_fluctuations):
    time_of_claps = []
    for i in range(len(body_areas)):
        if ith_area_is_local_min(i, body_areas) and body_is_active(i, body_fluctuations):
            time_of_claps.append(seconds[i])

    return time_of_claps

# The correct version 
def ith_area_is_local_min(i, body_areas):
    is_local_min = True
    for step in range(STEPS_TO_THE_LEFT, STEPS_TO_THE_RIGHT):
        if i + step >= 0 and i + step < len(body_areas) and body_areas[i] > body_areas[i + step]:
            is_local_min = False

    return is_local_min

def body_is_active(i, body_fluctuations):
    activity_before = False
    activity_after = False
    for num in range(1, STEPS_TO_THE_RIGHT):
        if (i + num) < len(body_fluctuations) and body_fluctuations[i + num] > FLUCTUATION_THRESHOLD:
            activity_after = True

        if (i - num) >= 0 and body_fluctuations[i - num] < -FLUCTUATION_THRESHOLD:
            activity_before = True

    if activity_before and activity_after:
        return True
    else:
        return False

def find_flight_intervals(time_of_claps):
    flight_interval = (-1, -1)
    flight_intervals = []
    for i in range(len(time_of_claps)):
        num_claps_before, num_claps_after = find_num_claps_before_and_after(i, time_of_claps)

        if is_start_interval(num_claps_before, num_claps_after):
            if flight_interval[0] == -1:
                flight_interval = (time_of_claps[i], -1)

        if is_end_interval(num_claps_before, num_claps_after):
            if flight_interval[0] != -1 and flight_interval[1] == -1:
                flight_interval = (flight_interval[0], time_of_claps[i])

        if is_flight_interval(flight_interval):
            flight_intervals.append(flight_interval)
            flight_interval = (-1, -1)

    return flight_intervals

def find_num_claps_before_and_after(i, time_of_claps):
    current_time_of_clap = time_of_claps[i]
    time_before_limit = current_time_of_clap - SECOND_THRESHOLD
    time_after_limit = current_time_of_clap + SECOND_THRESHOLD
    
    num_claps_before = 0
    decrementor = 1
    while (i - decrementor >= 0 and time_of_claps[i - decrementor] > time_before_limit):
        num_claps_before += 1
        decrementor += 1

    num_claps_after = 0
    incrementor = 1
    while(i + incrementor < len(time_of_claps) and time_of_claps[i + incrementor] < time_after_limit):
        num_claps_after += 1
        incrementor += 1

    return num_claps_before, num_claps_after

def is_start_interval(num_claps_before, num_claps_after):
    if num_claps_before < CLAP_THRESHOLD and num_claps_after > CLAP_THRESHOLD:
        return True 
    else:
        return False

def is_end_interval(num_claps_before, num_claps_after):
    if num_claps_before > CLAP_THRESHOLD and num_claps_after < CLAP_THRESHOLD:
        return True
    else:
        return False

def is_flight_interval(flight_interval):
    if flight_interval[0] != -1 and flight_interval[1] != -1:
        return True
    else:
        return False

def filter_flight_intervals(flight_intervals, duration_threshold):
    filtered_flight_intervals = []
    for flight_interval in flight_intervals:
        duration = flight_interval[1] - flight_interval[0]
        if duration_threshold < duration:
            filtered_flight_intervals.append(flight_interval)

    return filtered_flight_intervals
    	
def is_start_of_flight_interval(second, flight_intervals):
    index = g.binary_search(second, flight_intervals, compare_with_tuple)

    return True if index >= 0 else False

def is_during_flight_interval(second, flight_intervals):
    start_index = g.binary_search(second, flight_intervals, compare_with_tuple)
    end_index = g.binary_search(second, flight_intervals, FUNC)

    if (start_index >= 0 or end_index >= 0):
        return True
    else:
        start_insertion_index = (start_index + 1) * -1
        end_insertion_index = (end_index + 1) * -1

        if start_insertion_index - end_insertion_index == 1:
            return True

    return False

def is_end_of_flight_interval(second, flight_intervals):
    index = g.binary_search(second, flight_intervals, FUNC)
    
    return True if index >= 0 else False

def compare_with_tuple(tuple_, target, index=0):
    if target < tuple_[index]:
        return -1
    elif target == tuple_[index]:
        return 0
    else:
        return 1
