import cv2
import os
from glob import glob

root_folders = [
    'C:\\Users\\Administrator\\kichang\\data\\preprocessing\\change_to_path\\220624SlumpData',
    'C:\\Users\\Administrator\\kichang\\data\\preprocessing\\change_to_path\\220923_Additional_S120_S80',
    'C:\\Users\\Administrator\\kichang\\data\\preprocessing\\change_to_path\\221007Cheonan-new400data',
    'C:\\Users\\Administrator\\kichang\\data\\preprocessing\\change_to_path\\221209_SeoSeoul_HopperVideo'
]


path_part = [
    ['labeling_beginning16','images_beginning16'], 
    ['labeling_middle16', 'images_middle16'], 
    ['labeling_ending16', 'images_ending16']
]

def save_frames_from_video(input_path, output_folder_part):
    video_name = os.path.splitext(os.path.basename(input_path))[0]
    
    output_path  = input_path.split(os.sep)
    output_path[6] = output_folder_part
    output_path = os.sep.join(output_path)
    output_path = os.path.splitext(output_path)[0]

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    cap = cv2.VideoCapture(input_path)

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_file = os.path.join(output_path, f"{video_name}_frame{frame_count}.jpg")
        cv2.imwrite(frame_file, frame)

        frame_count += 1

    cap.release()

for main_folder in root_folders:
    for slump in ['S80', 'S120', 'S150', 'S180']:
        for input_folder_part, output_folder_part in path_part:

            # print(input_folder_part, output_folder_part)

            file_path = main_folder.split(os.sep)
            file_path[6] = input_folder_part
            input_folder = os.sep.join(file_path)
            input_folder = os.path.join(input_folder, slump)
            
            video_files = glob(os.path.join(input_folder, '*.avi'))
            print(input_folder)
            for video_file in video_files:
                
                print(video_file)
                save_frames_from_video(video_file, output_folder_part)