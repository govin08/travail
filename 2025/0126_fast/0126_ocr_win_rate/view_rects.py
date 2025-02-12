# view rectangles
import tkinter as tk

# 메인 창 생성
root = tk.Tk()
root.attributes('-alpha', 0.3)  # 전체 창 투명도 설정
root.attributes('-topmost', True)  # 항상 최상위에 표시
root.attributes('-fullscreen', True)  # 전체 화면
root.overrideredirect(True)  # 창 테두리 제거

# OCR 영역 좌표
top, bot = 130, 147
win_lef, win_rig = 359, 390
los_lef, los_rig = 395, 426

# 캔버스 생성
canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), 
                  highlightthickness=0, bg='black')
canvas.pack()

print(root.winfo_screenwidth())
print(root.winfo_screenheight())

# 직사각형 그리기
canvas.create_rectangle(win_lef, top, win_rig, bot, outline='blue', width=3)
canvas.create_rectangle(los_lef, top, los_rig, bot, outline='blue', width=3)

# ESC 키로 종료
def close(event):
    if event.keysym == 'Escape':
        root.quit()

root.bind('<Key>', close)

root.mainloop()
