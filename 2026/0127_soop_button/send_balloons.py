import pyautogui
import time
import keyboard
# import pyperclip

print('sending is now ready.')

x1, y1 = -517, 775
x2, y2 = 1314, 759
button_positions = {1:(x1,y1), 2:(x2,y2)}

def send_balloons(monitor_idx:int, num:str):
    x_star, y_star = button_positions[monitor_idx]
    pyautogui.click(x_star, y_star)
    time.sleep(0.3)

    pyautogui.press('backspace', presses=2, interval=0.2)
    keyboard.write(num)
    pyautogui.press('tab', presses=4, interval=0.1)
    time.sleep(0.2)

    keyboard.write("잘 들었습니다.")

    pyautogui.press('tab', presses=3, interval=0.1)
    pyautogui.press('enter')

keyboard.add_hotkey('F6', lambda: send_balloons(1, "5"))
keyboard.add_hotkey('F8', lambda: send_balloons(1, "10"))
keyboard.add_hotkey('F9', lambda: send_balloons(2, "5"))
keyboard.add_hotkey('F10', lambda: send_balloons(2, "10"))

keyboard.wait()  # 프로그램이 계속 실행되도록 유지