import sys
import os 
from glob import glob
import pandas as pd
import numpy as np
import cv2

root_folders = [
    # 'C:\\Users\\Administrator\\kichang\\data\\preprocessing\\labeling_48frame\\220624SlumpData',
    # 'C:\\Users\\Administrator\\kichang\\data\\preprocessing\\labeling_48frame\\220923_Additional_S120_S80',
    # 'C:\\Users\\Administrator\\kichang\\data\\preprocessing\\labeling_48frame\\221007Cheonan-new400data',
    # 'C:\\Users\\Administrator\\kichang\\data\\preprocessing\\labeling_48frame\\221209_SeoSeoul_HopperVideo'
    'C:\\Users\\Administrator\\kichang\\data\\preprocessing\\labeling_48frame\\240104_SeoSeoul'

    # 서서울 호퍼는 나중에 추가됨
]

# output_folders = [
#     # 'C:\\Users\\Administrator\\kichang\\preprocessing\\220624SlumpData',
#     'C:\\Users\\Administrator\\kichang\\preprocessing\\221007Cheonan-new400data',
#     # 'C:\\Users\\Administrator\\kichang\\preprocessing\\220923_Additional_S120_S80'
#     'C:\\Users\\Administrator\\kichang\\preprocessing\\221209_SeoSeoul_HopperVideo'
#     # 서서울 호퍼는 나중에 추가됨
# ]

S80 = []
S120 = []
S150 = []
S180 = []
S210 = []

for main_folder in root_folders:
    S80.extend(glob(os.path.join(main_folder, 'S80', '*.avi')))
    S120.extend(glob(os.path.join(main_folder, 'S120', '*.avi')))
    S150.extend(glob(os.path.join(main_folder, 'S150', '*.avi')))
    S180.extend(glob(os.path.join(main_folder, 'S180', '*.avi')))
    S210.extend(glob(os.path.join(main_folder, 'S210', '*.avi')))


# label=[0]*len(S80)+[1]*len(S120)+[2]*len(S150)+[3]*len(S180)
# label 0 for S80, 1 for S120, 2 for S150, 3 for S180
data_list = S80 + S120 + S150 + S180 + S210
# formatted_data = [f"{video_path} {lbl}" for video_path, lbl in zip(data_list, label)]

# df = pd.DataFrame(zip(S80+S120+S150+S180,label), columns=('file', 'label'))
print('S80 video', len(S80))
print('S120 video', len(S120))
print('S150 video', len(S150))
print('S180 video', len(S180))
print('S210 video', len(S210))


# 80 video 127
# S120 video 238
# S150 video 203
# S180 video 192

# print(formatted_data)

# 동영상 파일 경로 data_list

# 저장할 프레임의 범위 설정
# start_frame = 1
# end_frame = 16

# split as 3 parts at once
replay = [[0, 16, 'labeling_beginning16'],[16, 32, 'labeling_middle16'], [32, 48, 'labeling_ending16']]
# replay = [[16,31, 'labeling_middle16'],[32, 47, 'labeling_ending16']]

    # 동영상 불러오기
for start_frame, end_frame, path_part in replay:
        
    for video_path in data_list:

        path_parts = video_path.split(os.sep)
        path_parts[6] = path_part # output folder directory change instead of data
        output_path = os.sep.join(path_parts)

        cap = cv2.VideoCapture(video_path)

            # VideoWriter 객체 생성을 위한 설정
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # output file name
        out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

        current_frame = 0
        while cap.isOpened():
            ret, frame = cap.read()
            
            if not ret:
                print("Error in reading video!!!")
                break

            if start_frame <= current_frame <= end_frame:
                out.write(frame)

            current_frame += 1
            if current_frame > end_frame:
                break

        # 자원 해제
        cap.release()
        out.release()
