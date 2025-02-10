import keyboard, subprocess, sys, os, argparse, pyautogui
script_dir = os.path.dirname(os.path.abspath(__file__))
script_path = os.path.join(script_dir, "accumulator.py")

print('runner is now ready.')

def run_accumulator():
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


keyboard.add_hotkey('F8', run_accumulator)
keyboard.on_press_key('F9', lambda _: select_zerg())

keyboard.wait()  # 프로그램이 계속 실행되도록 유지