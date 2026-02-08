import pydirectinput
import argparse
import keyboard

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--n_towns', type=int, default=1)
args = parser.parse_args()

print('taverning is now ready.')

def tavern(n_towns:int):
    pydirectinput.press('esc', presses=2, interval=0.1)
    pydirectinput.press('l', interval=0.1)
    pydirectinput.press('enter', interval=0.1)
    pydirectinput.press('s', interval=0.1)
    pydirectinput.press('enter', interval=0.1)
    for _ in range(n_towns):
        pydirectinput.press('t', interval=0.1)
    pydirectinput.press('enter', interval=0.1)

keyboard.add_hotkey('F6', lambda: tavern(args.n_towns))

keyboard.wait()