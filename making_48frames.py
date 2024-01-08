# Making 48frames after labeled trim
import cv2
import numpy as np
import os
from glob import glob

def make_uniform_frames(video_path, output_path, target_frames=48):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Failed to open video: {video_path}")
        return

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    selected_frames = np.linspace(0, total_frames - 1, target_frames, dtype=int)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, cap.get(cv2.CAP_PROP_FPS),
                          (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

    for frame_idx in selected_frames:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if ret:
            out.write(frame)
        else:
            break

    cap.release()
    out.release()

root_folders = [
    'C:\\Users\\Administrator\\kichang\\data\\preprocessing\\labeling_trim\\220624SlumpData',
    'C:\\Users\\Administrator\\kichang\\data\\preprocessing\\labeling_trim\\220923_Additional_S120_S80',
    # 'C:\\Users\\Administrator\\kichang\\data\\preprocessing\\labeling_trim\\221007Cheonan-new400data',
    # 'C:\\Users\\Administrator\\kichang\\data\\preprocessing\\labeling_trim\\221209_SeoSeoul_HopperVideo'
]

for main_folder in root_folders:
    for speed in ['S80', 'S120', 'S150', 'S180']:
        video_files = glob(os.path.join(main_folder, speed, '*.avi'))

        for video_file in video_files:
            if os.path.exists(video_file):
                # path_parts = video_path.split(os.sep)
                # path_parts[4] = 'preprocessing\\end_20_frames' # output folder directory change instead of data
                # output_path = os.sep.join(path_parts)
                output_video_path = video_file.split(os.sep)
                output_video_path[6] = 'labeling_48frame'
                output_video_path = os.sep.join(output_video_path)
                output_video = f"{output_video_path}_48frame_extracted.avi"
                make_uniform_frames(video_file, output_video)
                print("Successfully saved!!")
            else:
                print(f"Labels file not found for {video_file}")
