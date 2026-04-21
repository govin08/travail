# v2 : Ctrl+F 기능 추가, Ctrl+H -> Ctrl+R
# v2.1 : 서식 -> 보기, 글꼴항목 없애기, 확대 및 축소 기능

import tkinter as tk
from tkinter import filedialog, messagebox, font
import os

class Notepad:
    def __init__(self, root):
        self.root = root
        self.root.title("메모장")
        self.root.geometry("800x600")
        self.current_file = None
        self.is_modified = False

        self._build_menu()
        self._build_editor()
        self._build_statusbar()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    # ── UI 구성 ─────────────────────────────────────────

    def _build_menu(self):
        menubar = tk.Menu(self.root)

        # 파일
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="새로 만들기",  accelerator="Ctrl+N", command=self.new_file)
        file_menu.add_command(label="열기...",       accelerator="Ctrl+O", command=self.open_file)
        file_menu.add_command(label="저장",          accelerator="Ctrl+S", command=self.save_file)
        file_menu.add_command(label="다른 이름으로 저장...", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="종료",          command=self.on_close)
        menubar.add_cascade(label="파일", menu=file_menu)

        # 편집
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="실행 취소",    accelerator="Ctrl+Z", command=lambda: self.text.edit_undo())
        edit_menu.add_command(label="다시 실행",    accelerator="Ctrl+Y", command=lambda: self.text.edit_redo())
        edit_menu.add_separator()
        edit_menu.add_command(label="잘라내기",     accelerator="Ctrl+X", command=lambda: self.text.event_generate("<<Cut>>"))
        edit_menu.add_command(label="복사",         accelerator="Ctrl+C", command=lambda: self.text.event_generate("<<Copy>>"))
        edit_menu.add_command(label="붙여넣기",     accelerator="Ctrl+V", command=lambda: self.text.event_generate("<<Paste>>"))
        edit_menu.add_command(label="모두 선택",    accelerator="Ctrl+A", command=lambda: self.text.tag_add("sel", "1.0", "end"))
        edit_menu.add_separator()
        edit_menu.add_command(label="찾기...",        accelerator="Ctrl+F", command=self.find)
        edit_menu.add_command(label="찾기/바꾸기...", accelerator="Ctrl+R", command=self.find_replace)
        menubar.add_cascade(label="편집", menu=edit_menu)

        # 보기
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="확대", accelerator="Ctrl++", command=self.zoom_in)
        view_menu.add_command(label="축소", accelerator="Ctrl+-", command=self.zoom_out)
        view_menu.add_command(label="기본 크기로", accelerator="Ctrl+0", command=self.zoom_reset)
        view_menu.add_separator()
        self.word_wrap = tk.BooleanVar(value=True)
        view_menu.add_checkbutton(label="자동 줄바꿈", variable=self.word_wrap, command=self.toggle_wrap)
        menubar.add_cascade(label="보기", menu=view_menu)

        self.root.config(menu=menubar)

        # 단축키
        self.root.bind("<Control-n>", lambda e: self.new_file())
        self.root.bind("<Control-o>", lambda e: self.open_file())
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Control-f>", lambda e: self.find())
        self.root.bind("<Control-r>", lambda e: self.find_replace())
        self.root.bind("<Control-plus>", lambda e: self.zoom_in())
        self.root.bind("<Control-minus>", lambda e: self.zoom_out())
        self.root.bind("<Control-0>", lambda e: self.zoom_reset())
        self.root.bind("<Control-MouseWheel>", self._on_zoom_wheel)



    def _build_editor(self):
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True)

        self.text = tk.Text(
            frame, wrap="word", undo=True,
            font=("맑은 고딕", 11), relief="flat",
            padx=6, pady=6
        )
        scrollbar = tk.Scrollbar(frame, command=self.text.yview)
        self.text.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)

        self.text.bind("<<Modified>>", self._on_text_change)
        self.text.bind("<KeyRelease>", self._update_status)
        self.text.bind("<Control-MouseWheel>", self._on_zoom_wheel)

    def _build_statusbar(self):
        self.status = tk.Label(
            self.root, text="줄 1, 열 1",
            anchor="e", padx=8, relief="sunken"
        )
        self.status.pack(side="bottom", fill="x")

    # ── 파일 작업 ────────────────────────────────────────

    def new_file(self):
        if self._check_save(): return
        self.text.delete("1.0", "end")
        self.current_file = None
        self.root.title("메모장")
        self.is_modified = False

    def open_file(self):
        if self._check_save(): return
        path = filedialog.askopenfilename(
            filetypes=[("텍스트 파일", "*.txt"), ("모든 파일", "*.*")]
        )
        if path:
            with open(path, encoding="utf-8") as f:
                self.text.delete("1.0", "end")
                self.text.insert("1.0", f.read())
            self.current_file = path
            self.root.title(f"{os.path.basename(path)} - 메모장")
            self.is_modified = False

    def save_file(self):
        if self.current_file:
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(self.text.get("1.0", "end-1c"))
            self.is_modified = False
            title = self.root.title() # 제목에서 *제거
            if title.startswith("*"):
                self.root.title(title[1:])
        else:
            self.save_as()

    def save_as(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("텍스트 파일", "*.txt"), ("모든 파일", "*.*")]
        )
        if path:
            self.current_file = path
            self.save_file()
            self.root.title(f"{os.path.basename(path)} - 메모장")

    # ── 편집 기능 ────────────────────────────────────────

    def _build_find_core(self, win, find_var):
        """찾기 공통 로직 — matches, go_to, next_match, do_find 반환"""
        self.text.tag_configure("highlight", background="yellow")
        self.text.tag_configure("current", background="orange")

        matches = []
        current_idx = [-1]

        count_label = tk.Label(win, text="")

        def do_find():
            self.text.tag_remove("highlight", "1.0", "end")
            self.text.tag_remove("current", "1.0", "end")
            matches.clear()
            current_idx[0] = -1
            keyword = find_var.get()
            if not keyword:
                count_label.config(text="")
                return
            start = "1.0"
            while True:
                pos = self.text.search(keyword, start, stopindex="end")
                if not pos:
                    break
                end = f"{pos}+{len(keyword)}c"
                self.text.tag_add("highlight", pos, end)
                matches.append((pos, end))
                start = end
            if matches:
                current_idx[0] = 0
                go_to(0)
            else:
                count_label.config(text="없음")

        def go_to(idx):
            self.text.tag_remove("current", "1.0", "end")
            pos, end = matches[idx]
            self.text.tag_add("current", pos, end)
            self.text.see(pos)
            count_label.config(text=f"{idx + 1} / {len(matches)}")

        def next_match(e=None):
            if not matches:
                do_find()
                return
            current_idx[0] = (current_idx[0] + 1) % len(matches)
            go_to(current_idx[0])

        def cleanup():
            self.text.tag_remove("highlight", "1.0", "end")
            self.text.tag_remove("current", "1.0", "end")
            win.destroy()

        return count_label, do_find, next_match, matches, current_idx, cleanup

    def find(self):
        win = tk.Toplevel(self.root)
        win.title("찾기")
        win.resizable(False, False)

        tk.Label(win, text="찾기:").grid(row=0, column=0, padx=8, pady=6, sticky="e")
        find_var = tk.StringVar()
        entry = tk.Entry(win, textvariable=find_var, width=24)
        entry.grid(row=0, column=1, padx=8)
        entry.focus()

        count_label, do_find, next_match, _, _, cleanup = self._build_find_core(win, find_var)
        count_label.grid(row=1, column=0, columnspan=3, pady=4)

        entry.bind("<Return>", next_match)
        tk.Button(win, text="찾기", command=next_match).grid(row=0, column=2, padx=8)
        win.protocol("WM_DELETE_WINDOW", cleanup)

    def find_replace(self):
        win = tk.Toplevel(self.root)
        win.title("찾기/바꾸기")
        win.resizable(False, False)

        tk.Label(win, text="찾기:").grid(row=0, column=0, padx=8, pady=6, sticky="e")
        find_var = tk.StringVar()
        entry = tk.Entry(win, textvariable=find_var, width=24)
        entry.grid(row=0, column=1, padx=8)
        entry.focus()

        tk.Label(win, text="바꾸기:").grid(row=1, column=0, padx=8, pady=4, sticky="e")
        rep_var = tk.StringVar()
        tk.Entry(win, textvariable=rep_var, width=24).grid(row=1, column=1, padx=8)

        count_label, do_find, next_match, matches, current_idx, cleanup = self._build_find_core(win, find_var)
        count_label.grid(row=2, column=0, columnspan=3, pady=4)

        def do_replace(e=None):
            if not matches:
                do_find()
                return
            pos, end = matches[current_idx[0]]
            self.text.delete(pos, end)
            self.text.insert(pos, rep_var.get())
            do_find()

        entry.bind("<Return>", next_match)
        tk.Button(win, text="찾기",   command=next_match).grid(row=0, column=2, padx=8)
        tk.Button(win, text="바꾸기", command=do_replace).grid(row=1, column=2, padx=8)
        win.protocol("WM_DELETE_WINDOW", cleanup)

    def toggle_wrap(self):
        self.text.configure(wrap="word" if self.word_wrap.get() else "none")

    def zoom_in(self):
        f = font.Font(font=self.text["font"])
        self.text.configure(font=(f.actual()["family"], f.actual()["size"] + 1))

    def zoom_out(self):
        f = font.Font(font=self.text["font"])
        size = f.actual()["size"]
        if size > 6:
            self.text.configure(font=(f.actual()["family"], size - 1))

    def zoom_reset(self):
        self.text.configure(font=("맑은 고딕", 11))

    def _on_zoom_wheel(self, e):
        if e.delta > 0:
            self.zoom_in()
        else:
            self.zoom_out()
        return "break"  # 기본 스크롤 동작 막기

    # ── 내부 유틸 ────────────────────────────────────────

    def _on_text_change(self, _=None):
        if self.text.edit_modified():
            self.is_modified = True
            title = self.root.title()
            if not title.startswith("*"):
                self.root.title("*" + title)
            self.text.edit_modified(False)

    def _update_status(self, _=None):
        pos = self.text.index("insert")
        line, col = pos.split(".")
        chars = len(self.text.get("1.0", "end-1c"))
        self.status.config(text=f"줄 {line}, 열 {int(col)+1}   문자 수: {chars}")

    def _check_save(self):
        if self.is_modified:
            ans = messagebox.askyesnocancel("저장", "저장하지 않은 내용이 있습니다. 저장할까요?")
            if ans is True:
                self.save_file()
            elif ans is None:
                return True
        return False

    def on_close(self):
        if not self._check_save():
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = Notepad(root)
    root.mainloop()