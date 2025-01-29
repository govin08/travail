import keyboard, subprocess, sys, os
script_dir = os.path.dirname(os.path.abspath(__file__))
script_path = os.path.join(script_dir, "accumulator.py")

def run_script():
    subprocess.run([sys.executable, script_path])

keyboard.add_hotkey('F8', run_script)
keyboard.wait()  # 프로그램이 계속 실행되도록 유지

