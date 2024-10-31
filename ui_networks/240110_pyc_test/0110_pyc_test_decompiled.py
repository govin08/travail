import numpy as np

# 두 개의 배열 생성
durs_A = np.array([37, 55, 45, 23])
durs_B = np.array([37, 55, 28, 40])

# 두 배열의 누적합 계산
cums_A = durs_A.cumsum()
cums_B = durs_B.cumsum()

# durs_A의 합계를 cycle에 저장
cycle = durs_A.sum()

# 빈 리스트 생성
detailed_cums = []

# cums_A와 cums_B의 고유한 요소들을 결합
combined_row = np.unique(np.concatenate((cums_A, cums_B)))

# combined_row의 각 요소 간 차이 계산
detailed_durations = np.concatenate(([combined_row[0]], np.diff(combined_row)))

# 결과 출력
print(detailed_durations)
