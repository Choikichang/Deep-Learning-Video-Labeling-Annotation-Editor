import os
import cv2
import json
from glob import glob

def create_labeled_video(video_path, labels_path, output_path):
    with open(labels_path, 'r') as file:
        labels = json.load(file)['labels']
        
        # for the check
        # print(len(labels))

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Failed to open video: {video_path}")
        return
        
    print(f'Video file successfully loaded!')

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, cap.get(cv2.CAP_PROP_FPS),
                          (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

    frame_number = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # for error ignore in SeoSeoulHopper 18-80-03(_150).avi
        # There is a labeling error when label turn 1 to 0 then one frame number is absent.
        # print(len(labels))
        if frame_number < len(labels) and labels[frame_number]['label'] == 1:
        # if labels[frame_number]['label'] == 1:
            # print(len(labels))
            # print(frame_number)
            out.write(frame)

        frame_number += 1

    cap.release()
    out.release()

root_folders = [
    # 'C:\\Users\\Administrator\\kichang\\data\\original\\220624SlumpData',
    # 'C:\\Users\\Administrator\\kichang\\data\\original\\220923_Additional_S120_S80',
    # 'C:\\Users\\Administrator\\kichang\\data\\original\\221007Cheonan-new400data',
    # 'C:\\Users\\Administrator\\kichang\\data\\original\\221209_SeoSeoul_HopperVideo'
    'C:\\Users\\Administrator\\kichang\\data\\compress\\240104_SeoSeoul'
]

for main_folder in root_folders:
    # for the test
    for speed in ['S80', 'S120', 'S150', 'S180', 'S210']: # just for fix error
    # for speed in ['S80', 'S120', 'S150', 'S180']: 

        labels_files = glob(os.path.join(main_folder, speed, '*.json'))

        for labels_file in labels_files:

            video_file = labels_file.rsplit('.', 1)[0]

            # # for 3time test
            # for i in range(3):

            if os.path.exists(labels_file):
                # path_parts = video_path.split(os.sep)
                # path_parts[4] = 'preprocessing\\end_20_frames' # output folder directory change instead of data
                # output_path = os.sep.join(path_parts)
                output_video_path = video_file.split(os.sep)
                output_video_path[5] = 'preprocessing\\labeling_trim'
                output_video_path = os.sep.join(output_video_path)
                output_video = f"{output_video_path}_labeled.avi"
                create_labeled_video(video_file, labels_file, output_video)
            else:
                print(f"Labels file not found for {video_file}")