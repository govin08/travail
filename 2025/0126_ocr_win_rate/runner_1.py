import keyboard, subprocess, sys, os, argparse

parser = argparse.ArgumentParser()
parser.add_argument('--aug', '-a', type=lambda x:x.lower() == 'true', default=True)
parser.add_argument('--n_sam', '-n', type=int, default=10)
args = parser.parse_args()

script_dir = os.path.dirname(os.path.abspath(__file__))
script_path = os.path.join(script_dir, "accumulator_1.py")

print('runner is now ready.')
def run_script(aug=args.aug, n_sam=args.n_sam):
    print(f"aug : {aug}")
    print(f"n_sam : {n_sam}")
    sys.stdout.flush()  # 버퍼 즉시 출력
    result = subprocess.run(
        [sys.executable, script_path, '--aug', str(aug), '--n_sam', str(n_sam)],
        capture_output=True, text=True)
    print(result.stdout)
    sys.stdout.flush()  # 버퍼 즉시 출력

keyboard.add_hotkey('F8', run_script)
keyboard.wait()  # 프로그램이 계속 실행되도록 유지