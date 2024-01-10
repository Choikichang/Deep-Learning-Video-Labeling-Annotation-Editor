import cv2
import os
from glob import glob
from moviepy.editor import VideoFileClip

root_folders = [
    # 'C:\\Users\\Administrator\\kichang\\data\\preprocessing\\change_to_path\\220624SlumpData',
    # 'C:\\Users\\Administrator\\kichang\\data\\preprocessing\\change_to_path\\220923_Additional_S120_S80',
    # 'C:\\Users\\Administrator\\kichang\\data\\preprocessing\\change_to_path\\221007Cheonan-new400data',
    # 'C:\\Users\\Administrator\\kichang\\data\\preprocessing\\change_to_path\\221209_SeoSeoul_HopperVideo',
    'C:\\Users\\Administrator\\kichang\\data\\change_to_path\\240104_SeoSeoul'
]

path_part = [
    ['original','compress'], 
#     ['labeling_middle16', 'images_middle16'], 
#     ['labeling_ending16', 'images_ending16']
]


def compress_video(input_path, output_folder_part,  target_resolution):
    video_name = os.path.splitext(os.path.basename(input_path))[0]
    
    output_path = input_path.split(os.sep)
    output_path[5] = output_folder_part
    output_dir = os.sep.join(output_path[:-1])
    output_file = os.path.join(output_dir, video_name + "_compressed.mp4")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


    clip = VideoFileClip(input_path)

        # Calculate the new resolution to maintain the aspect ratio
    width, height = clip.size
    aspect_ratio = width / height
    new_height = target_resolution
    new_width = int(new_height * aspect_ratio)

    # Resize the video
    clip_resized = clip.resize(newsize=(new_width, new_height))

    # Write the resized video to the output file
    clip_resized.write_videofile(output_file, fps=30)



###########################################################################




for main_folder in root_folders:
    for slump in [ 'S210']:
        for input_folder_part, output_folder_part in path_part:

            # print(input_folder_part, output_folder_part)

            file_path = main_folder.split(os.sep)
            file_path[5] = input_folder_part
            input_folder = os.sep.join(file_path)
            input_folder = os.path.join(input_folder, slump)
            
            video_files = glob(os.path.join(input_folder, '*.avi'))
            print(input_folder)
            for video_file in video_files:
                
                print(video_file)
                compress_video(video_file, output_folder_part, 480)