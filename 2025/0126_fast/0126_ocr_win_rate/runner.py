import keyboard, subprocess, sys, os, pyautogui
from datetime import datetime as DT
from PIL import ImageGrab


print('runner is now ready.')

def run_accumulator():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, "accumulator.py")
    subprocess.run([sys.executable, script_path])

def select_zerg():
    x_rac, y_rac, y_zer = 835, 354, 366
    x_col, y_col, y_gre = 910, 354, 466
    pyautogui.sleep(0.2)
    pyautogui.click(x_rac, y_rac)
    pyautogui.click(x_rac, y_zer)
    pyautogui.click(x_col, y_col)
    pyautogui.click(x_col, y_gre)
    print('F9 : race and color selected.')

def collect_rects():
    the_positions = {1: [570, 130, 650, 150],
                     2: [570, 179, 650, 199],
                     3: [570, 228, 650, 248],
                     4: [570, 310, 650, 330],
                     5: [570, 359, 650, 379],
                     6: [570, 408, 650, 428]}
    timestamp = DT.now().strftime('%m%d_%H%M')
    for num, pos in the_positions.items():
        print(pos)
        capture = ImageGrab.grab(bbox=tuple(pos))
        filename = str(num) + '_' + timestamp
        # capture.save(f'./captured_rects/{filename}.png')
        capture.save(f'../0212_ban_vpn/captured_rects/{filename}.png')
        print(filename)

keyboard.add_hotkey('F8', run_accumulator)
keyboard.add_hotkey('F9', select_zerg)
keyboard.add_hotkey('F12', collect_rects)

keyboard.wait()  # 프로그램이 계속 실행되도록 유지