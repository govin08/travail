from PIL import ImageGrab
import pytesseract, csv, os
from datetime import datetime as DT
from itertools import product
from collections import Counter

def load_log(log_path):
    # 최신 승수와 패수 불러오기
    with open(log_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        last_line = list(reader)[-1]
        prev_n_win = int(last_line[3])
        prev_n_los = int(last_line[4])
    return prev_n_win, prev_n_los

def capture_section(ocr_dir, lef, top, rig, bot, name, config = '-c tessedit_char_whitelist=0123456789',augmentation=False):
    section = ImageGrab.grab(bbox=(lef, top, rig, bot))
    # 캡처한 이미지를 파일로 저장
    section.save(os.path.join(ocr_dir, f"{name}.png"))
    if not augmentation:
        # OCR을 사용하여 화면의 숫자를 문자열 형태로 변환
        num = pytesseract.image_to_string(
            section,
            config=config # '-c tessedit_char_whitelist=0123456789'
            ).strip() # the number of wins
        return num
    else:
            # OCR 위치 후보 지정
        sep = 1
        lefs = range(lef - sep, lef + sep + 1)
        rigs = range(rig - sep, rig + sep + 1)
        tops = range(top - sep, top + sep + 1)
        bots = range(bot - sep, bot + sep + 1)
        
        locs = list(product(lefs, tops, rigs, bots))

        nums = []
        for (lef, top, rig, bot) in locs:
            num = pytesseract.image_to_string(
                section,
                config=config # '-c tessedit_char_whitelist=0123456789'
                ).strip() # the number of wins
            nums.append(num)
        print(nums)
        counts = Counter(nums)
        freq_num, frequency = counts.most_common(1)[0]
        print(f"OCR 결과 : {freq_num}, 빈도 : {frequency} / {(2 * sep+1)**4}")
        return freq_num

def validate_numbers(n_win, n_los):
    try:
        n_win, n_los = int(n_win), int(n_los)
    except ValueError:
        print("Error: Failed to recognize valid numbers from the screen.")
        print(f"Detected values: n_win='{n_win}', n_los='{n_los}'")
        exit()
    return n_win, n_los

def calculate(n_win, n_los):
    # 승률, 승패차이
    win_rate = round(n_win / (n_win + n_los) * 100, 3)
    difference = n_win - n_los
    print(f"win_rate : {win_rate}")
    print(f"difference : {difference}")
    return win_rate, difference

def update_log(prev_n_win, prev_n_los, n_win, n_los, win_rate, difference, log_path):
    timestamp = DT.now().strftime('%Y_%m_%d_%H%M')
    # 로그파일 업데이트
    with open(log_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if (prev_n_win, prev_n_los) != (n_win, n_los):
            writer.writerow([timestamp, win_rate, difference, n_win, n_los])
            print("log file is now updated")
        else:
            print("no change in stats")

def main(augmentation=False):
    print("")
    print("========viewing the screen========")
    # 프로그램 경로
    ocr_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(ocr_dir, "log.csv")
    
    # 로그파일 로드
    prev_n_win, prev_n_los = load_log(log_path)
    
    # OCR 위치 지정
    top, bot = 131, 147
    win_lef, win_rig = 359, 391
    los_lef, los_rig = 395, 427
    
    n_win = capture_section(ocr_dir, win_lef, top, win_rig, bot, 'section_win', augmentation = augmentation)
    n_los = capture_section(ocr_dir, los_lef, top, los_rig, bot, 'section_los', augmentation = augmentation)
    n_win, n_los = validate_numbers(n_win, n_los)
    print(n_win, n_los)
    win_rate, difference = calculate(n_win, n_los)
    update_log(prev_n_win, prev_n_los, n_win, n_los, win_rate, difference, log_path)
    
if __name__ == "__main__":
    main(augmentation=False)