import pandas as pd
import matplotlib.pyplot as plt

# CSV 파일 불러오기
df = pd.read_csv("~/Git/Seoseoul_slump_time_table.csv")  # 파일 경로를 적절히 수정하세요.

# S120과 S150 데이터 필터링
s120_data = df[df["슬럼프"] == "S120"]
s150_data = df[df["슬럼프"] == "S150"]
s180_data = df[df["슬럼프"] == "S180"]
s210_data = df[df["슬럼프"] == "S210"]

# 그래프 생성
plt.figure(figsize=(10, 6))
plt.scatter(s120_data.index, s120_data["labeling"]/30, label="S120")
plt.scatter(s150_data.index, s150_data["labeling"]/30, label="S150")
plt.scatter(s180_data.index, s180_data["labeling"]/30, label="S180")
plt.scatter(s210_data.index, s210_data["labeling"]/30, label="S210")

plt.xlabel("data index")
plt.ylabel("Discharge time")
plt.title("Slump")
plt.legend()
plt.tight_layout()
plt.show()
