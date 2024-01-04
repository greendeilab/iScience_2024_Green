import numpy as np

def locate_all(predictions, mapping, important_labels):
    all_object_locations = {}
    for second, prediction_info in predictions.items():
        object_locations = find_object_locations(prediction_info, mapping, important_labels)
        
        if object_locations != None:
            all_object_locations.setdefault(second, object_locations)

    return all_object_locations

def find_object_locations(prediction_info, mapping, important_labels):
    '''
        Will attempt to find the corresponding box for each key in the mapping.
        If an object is not found and it is considered important (i.e., required for some operation), 
        None will be returned.
    '''
    boxes, scores, labels = separate_prediction_info(prediction_info)
    boxes, labels = filter_predictions(mapping, boxes, scores, labels)
    object_locations = {}
    for object_label, label_num in mapping.items():
        try:
            box_index = labels.index(label_num)
        except ValueError:
            if object_label in important_labels:
                return None
            else:
                box = []
        else:
            box = boxes[box_index]

        object_locations.setdefault(object_label, box)
        
    return object_locations

def separate_prediction_info(prediction_info):
    boxes, scores, labels = [], [], []
    for item in prediction_info:
        boxes.append(item[:4].tolist())
        scores.append(item[4])
        labels.append(item[5])

    return [boxes, scores, labels]

def filter_predictions(mapping, boxes, scores, labels):
    ''' 
        If multiple boxes of the same object are present, 
        choose the one with the highest score.
    '''
    best_boxes = []
    best_labels = []
    labels = np.array(labels)
    for object_label, label_num in mapping.items():
        num_labels = len(labels[labels == label_num])
        if num_labels == 0: 
            continue
            
        if num_labels > 1:
            best_box = find_best_box(boxes, scores, labels, label_num)
        elif num_labels == 1:
            label_index = labels.tolist().index(label_num)
            best_box = boxes[label_index]

        best_boxes.append(best_box)
        best_labels.append(label_num)

    return [best_boxes, best_labels]

def find_best_box(boxes, scores, labels, label_num):
    ''' 
        Returns the box with the highest score for a specified label.
    '''
    label_boxes = np.array(boxes)[labels == label_num].tolist()
    label_scores = np.array(scores)[labels == label_num].tolist()
    max_score = max(label_scores)
    max_index = label_scores.index(max_score)

    return label_boxes[max_index]

def get_middle_location(locations):
    middle_location = None
    XMIN = 0
    boxes = [box for box in locations.values() if box != []]
    if len(boxes) > 0:
        sorted_boxes = sorted(boxes, key=lambda box: box[XMIN])
        median_box_index = int(len(sorted_boxes) / 2)
        middle_location = sorted_boxes[median_box_index]

    return middle_location

def filter_object_locations(all_object_locations, label):
    filtered_object_locations = {}
    for second, locations in all_object_locations.items():
        box = locations[label]
        filtered_object_locations.setdefault(second, locations[label])

    return filtered_object_locations

