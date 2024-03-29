import pandas as pd
from glob import glob
import os
import json

root_folders = [
    '/media/choi/HDD1/mmaction2/data/compress/240104_SeoSeoul',
    '/media/choi/HDD1/mmaction2/data/original/220624SlumpData',
    '/media/choi/HDD1/mmaction2/data/original/220923_Additional_S120_S80',
    '/media/choi/HDD1/mmaction2/data/original/221007Cheonan-new400data',
    '/media/choi/HDD1/mmaction2/data/original/221209_SeoSeoul_HopperVideo'
]

result_data = []

for main_folder in root_folders:
    # for the test
    for speed in ['S80', 'S120', 'S150', 'S180', 'S210']: # just for fix error

        labels_files = glob(os.path.join(main_folder, speed, '*.json'))

        for json_file in labels_files:
            with open(json_file, 'r') as f:
                data = json.load(f)

            # 1로 라벨링된 데이터 개수 세기
            label_count = sum(1 for label in data["labels"] if label["label"] == 1)

            # CSV 데이터를 딕셔너리 형태로 추가
            result_data.append({
                "동영상 디렉토리": os.path.dirname(json_file),
                "슬럼프": speed,
                "동영상 이름": os.path.basename(json_file),
                "프레임 숫자": len(data["labels"]),
                "1로 라벨링된 데이터 개수": label_count
            })

# 결과 데이터를 DataFrame으로 변환
df = pd.DataFrame(result_data)

# CSV 파일로 저장
df.to_csv("slump_time_table.csv", index=False)