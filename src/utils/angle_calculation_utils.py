import math

def calculate(box_interest, box_reference):
    ''' 
        Finds angle between two boxes in an image. Since image quadrant is a vertical reflection
        of the normal quadrant, the absolute angle needs to be taken and then adjusted accordingly. 
    '''
    center_interest, center_reference = calculate_box_centers(box_interest, box_reference)
    x, y = calculate_xy_difference(center_interest, center_reference)
    angle = calculate_absolute_angle(x, y)
    quadrant = calculate_image_quadrant(x, y)
    return correct_angle_based_on_quadrant(angle, quadrant)        

def calculate_box_centers(box_interest, box_reference):
    center_interest = get_center(box_interest)
    center_reference = get_center(box_reference)
    return [center_interest, center_reference]

def get_center(box):
    XMIN, YMIN, XMAX, YMAX = 0, 1, 2, 3 
    center_x = (box[XMIN] + box[XMAX]) / 2
    center_y = (box[YMIN] + box[YMAX]) / 2
    return [center_x, center_y]
        
def calculate_xy_difference(center_interest, center_reference):
    x = center_interest[0] - center_reference[0]
    y = center_interest[1] - center_reference[1]
    return [x, y]
        
def calculate_absolute_angle(x, y):
    try:
        radians = math.atan(abs(y) / abs(x))
    except ZeroDivisionError:
        angle = 90
    else:
        angle = math.degrees(radians)
    return angle

def calculate_image_quadrant(x, y):
    if x >= 0 and y <= 0:
        quadrant = 1
    elif x < 0 and y <= 0:
        quadrant = 2
    elif x < 0 and y > 0:
        quadrant = 3 
    else:
        quadrant = 4
    return quadrant

def calculate_normal_quadrant(x, y):
    if x >= 0 and y >= 0:
        quadrant = 1 
    elif x < 0 and y >= 0:
        quadrant = 2
    elif x < 0 and y < 0:
        quadrant = 3
    else:
        quadrant = 4
    return quadrant

def correct_angle_based_on_quadrant(angle, quadrant):
    if quadrant == 1:
        pass
    elif quadrant == 2:
        angle = 180 - angle
    elif quadrant == 3:
        angle += 180
    else:
        angle = 360 - angle
    return angle
