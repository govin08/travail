import ctypes, subprocess, sys, os, time, threading
import pyautogui
from datetime import datetime as DT
from PIL import ImageGrab

user32 = ctypes.windll.user32

def run_accumulator():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, "accumulator.py")
    subprocess.run([sys.executable, script_path])

def select_zerg():
    x_rac, y_rac, y_zer = 835, 354, 366
    x_col, y_col, y_gre = 910, 354, 466
    pyautogui.sleep(0.2)
    pyautogui.click(x_rac, y_rac); pyautogui.click(x_rac, y_zer)
    pyautogui.click(x_col, y_col); pyautogui.click(x_col, y_gre)
    print('F9 : race(zerg) and color selected.')

def select_terran():
    x_rac, y_rac, y_ter = 835, 354, 376
    x_col, y_col, y_gre = 910, 354, 466
    pyautogui.sleep(0.2)
    pyautogui.click(x_rac, y_rac); pyautogui.click(x_rac, y_ter)
    pyautogui.click(x_col, y_col); pyautogui.click(x_col, y_gre)
    print('F10 : race(terran) and color selected.')

def select_protoss():
    x_rac, y_rac, y_tos = 835, 354, 386
    x_col, y_col, y_gre = 910, 354, 466
    pyautogui.sleep(0.2)
    pyautogui.click(x_rac, y_rac); pyautogui.click(x_rac, y_tos)
    pyautogui.click(x_col, y_col); pyautogui.click(x_col, y_gre)
    print('F11 : race(protoss) and color selected.')

def collect_rects():
    the_positions = {1: [570, 130, 650, 150], 2: [570, 179, 650, 199],
                     3: [570, 228, 650, 248], 4: [570, 310, 650, 330],
                     5: [570, 359, 650, 379], 6: [570, 408, 650, 428]}
    timestamp = DT.now().strftime('%m%d_%H%M')
    for num, pos in the_positions.items():
        capture = ImageGrab.grab(bbox=tuple(pos))
        filename = str(num) + '_' + timestamp
        capture.save(f'../0212_ban_vpn/captured_rects/{filename}.png')
        print(filename)

# 가상키 코드 매핑 (F8~F12)
HOTKEYS = {0x77: run_accumulator, 0x78: select_zerg, 0x79: select_terran,
           0x7A: select_protoss, 0x7B: collect_rects}

def run_handler(fn):
    # 블로킹 작업(subprocess 등)이 폴링 루프를 막지 않도록 별도 스레드에서 실행
    threading.Thread(target=fn, daemon=True).start()

def main():
    print('runner is now ready. (polling mode)')
    prev = {vk: False for vk in HOTKEYS}
    while True:
        for vk, fn in HOTKEYS.items():
            down = bool(user32.GetAsyncKeyState(vk) & 0x8000)
            if down and not prev[vk]:      # 눌리는 순간(edge)에만 1회 실행
                run_handler(fn)
            prev[vk] = down
        time.sleep(0.02)

if __name__ == '__main__':
    main()