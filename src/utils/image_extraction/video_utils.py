import os
import cv2 
import random as r

SIZE_OF_FRAME = 18000

def extract_and_save(file_directory, save_directory, video, num_frames_per_video, problematic_frames):
    video_size = get_video_size(file_directory, video)
    total_video_frames = get_total_video_frames(video, video_size)
    frame_extraction_probability = calculate_frame_extraction_probability(problematic_frames, num_frames_per_video, total_video_frames)

    extract_and_save_frames(file_directory, save_directory, video, num_frames_per_video, frame_extraction_probability, problematic_frames)

def get_video_size(file_directory, video):
    return os.path.getsize(f'{file_directory}/{video}')

def get_total_video_frames(video, video_size):
    try:
        return read_total_video_frames(video)
    except:
        return estimate_total_video_frames(video_size)

def read_total_video_frames(video):
    return int(video.get(cv2.CAP_PROP_FRAME_COUNT))

def estimate_total_video_frames(video_size):
    return int(video_size / SIZE_OF_FRAME)

def calculate_frame_extraction_probability(problematic_frames, num_frames_per_video, total_video_frames):
    # If the probability is too low, the app will take a long time extracting images so a threshold is required
    threshold_probability = 0.05
    length_problematic_frames = len(problematic_frames)
    if length_problematic_frames > 0:
        threshold_probability = 0.9
        probability = num_frames_per_video / length_problematic_frames
    else:
        probability = num_frames_per_video / total_video_frames

    return probability if probability > threshold_probability else threshold_probability 

def extract_and_save_frames(file_directory, save_directory, video, num_frames_per_video, frame_extraction_probability, problematic_frames):
    saved_num_frames = 0
    frame_num = 1
    opened_video = cv2.VideoCapture(f'{file_directory}/{video}')
    while opened_video.isOpened():
        reading_properly, frame = opened_video.read()

        if reading_properly and frame_is_selected(frame_num, frame_extraction_probability, problematic_frames):
            resized_frame = cv2.resize(frame, None, fx=0.5, fy=0.5)
            cv2.imwrite(f'{save_directory}/{video[:-4]}_{frame_num}.jpg', resized_frame)
            saved_num_frames += 1

        if saved_num_frames == num_frames_per_video:
            break

        frame_num += 1

    opened_video.release()
    cv2.destroyAllWindows()

def frame_is_selected(frame_num, frame_extraction_probability, problematic_frames, random_float=None):
    if not random_float:
        random_float = r.random()

    is_selected = False
    if problematic_frames:
        if frame_num in problematic_frames and random_float <= frame_extraction_probability:
            is_selected = True 
    else:
        if random_float <= frame_extraction_probability:
            is_selected = True
            
    return is_selected
