import numpy as np
# A, B로 나뉘어진 현시시간을 (4현시) 세부현시시간(5현시)로 바꾸는 코드
durs_A = np.array([37, 55, 45, 23])
durs_B = np.array([37, 55, 28, 40])
cums_A = durs_A.cumsum()
cums_B = durs_B.cumsum()
cycle = durs_A.sum()
detailed_cums = []
combined_row = np.unique(np.concatenate((cums_A, cums_B)))
detailed_durations = np.concatenate(([combined_row[0]], np.diff(combined_row)))
print(detailed_durations)