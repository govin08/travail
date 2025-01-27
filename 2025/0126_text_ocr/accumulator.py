from PIL import ImageGrab
import pytesseract, csv, os
from datetime import datetime as DT

print("")
print("========viewing the screen========")

# 로그파일 위치
ocr_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(ocr_dir, "log.csv")
# 최신 승수와 패수 불러오기
with open(log_path, 'r') as csvfile:
    reader = csv.reader(csvfile)
    last_line = list(reader)[-1]
    prev_n_win = int(last_line[3])
    prev_n_los = int(last_line[4])

# OCR 위치 지정
top, bottom = 131, 147
left_win, right_win = 359, 392
left_los, right_los = 395, 428
win_capture = ImageGrab.grab(bbox=(left_win, top, right_win, bottom))
los_capture = ImageGrab.grab(bbox=(left_los, top, right_los, bottom))
# OCR을 사용하여 승수, 패수를 문자열 형태로 변환
n_win = pytesseract.image_to_string(
    win_capture,
    config='-c tessedit_char_whitelist=0123456789'
    ).strip() # the number of wins
n_los = pytesseract.image_to_string(
    los_capture,
    config='-c tessedit_char_whitelist=0123456789'
    ).strip() # the number of losses
print(n_win, n_los)
try:
    n_win, n_los = int(n_win), int(n_los)
except ValueError:
    print("Error: Failed to recognize valid numbers from the screen.")
    print(f"Detected values: n_win='{n_win}', n_los='{n_los}'")
    exit()

# 승률, 승패차이, 현재시각
win_rate = round(n_win / (n_win + n_los) * 100, 3)
difference = n_win - n_los
timestamp = DT.now().strftime('%Y_%m_%d_%H%M')
# 로그파일 업데이트
with open(log_path, 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    if (prev_n_win, prev_n_los) != (n_win, n_los):
        writer.writerow([timestamp, win_rate, difference, n_win, n_los])
        print("log file is now updated")
    else:
        print("no change in stats")

print("win rate : ", win_rate, "%")
print("difference :", difference)