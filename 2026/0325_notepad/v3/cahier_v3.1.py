# v2 : Ctrl+F 기능 추가, Ctrl+H -> Ctrl+R
# v2.1 : 서식 -> 보기, 글꼴항목 없애기, 확대 및 축소 기능
# - 파일 작업 / 편집 / 찾기·바꾸기 / 보기(확대축소·자동줄바꿈)
# - 한글 IME 완전 지원 (QTextEdit 기반)
# - 상태표시줄 (줄·열·문자수)
# v3.0 : PyQt6 사용 (기존 : tkinter)
# v3.1 : 찾기 및 바꾸기 기능 추가, 붙여넣기시 기본서식으로 붙여넣기

import sys, os
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QMessageBox, QFileDialog, QStatusBar, QWidget, QVBoxLayout
from PyQt6.QtGui import QAction, QKeySequence, QFont
from PyQt6.QtCore import Qt, QEvent
from find_bar import FindBar

class Cahier(QMainWindow):
    BASE_FONT_SIZE = 11

    def __init__(self):
        super().__init__()
        self.current_file: str | None = None
        self.font_family = "맑은 고딕"
        self.font_size = self.BASE_FONT_SIZE

        self._build_central()
        self._build_menu()
        self._build_statusbar()

        self.setWindowTitle("cahier")
        self.resize(800, 600)


    # ── UI 구성 ──────────────────────────────

    def _build_central(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.editor = QTextEdit()
        self.editor.setFont(QFont(self.font_family, self.font_size))
        self.editor.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)

        self.find_bar = FindBar(self.editor, self)

        layout.addWidget(self.find_bar)
        layout.addWidget(self.editor)

        self.setCentralWidget(container)

        self.editor.document().contentsChanged.connect(self._on_modified)
        self.editor.cursorPositionChanged.connect(self._update_status)
        self.editor.installEventFilter(self)


    def _build_menu(self):
        mb = self.menuBar()

        # ── 파일
        fm = mb.addMenu("파일(&F)")
        fm.addAction(self._act("새로 만들기(&N)", "Ctrl+N", self.new_file))
        fm.addAction(self._act("열기(&O)...",     "Ctrl+O", self.open_file))
        fm.addAction(self._act("저장(&S)",        "Ctrl+S", self.save_file))
        fm.addAction(self._act("다른 이름으로 저장(&A)...", None, self.save_as))
        fm.addSeparator()
        fm.addAction(self._act("종료(&X)",        "Alt+F4", self.close))

        # ── 편집
        em = mb.addMenu("편집(&E)")
        em.addAction(self._act("실행 취소(&Z)", "Ctrl+Z", self.editor.undo))
        em.addAction(self._act("다시 실행(&Y)", "Ctrl+Y", self.editor.redo))
        em.addSeparator()
        em.addAction(self._act("잘라내기(&T)",  "Ctrl+X", self.editor.cut))
        em.addAction(self._act("복사(&C)",      "Ctrl+C", self.editor.copy))
        em.addAction(self._act("붙여넣기(&P)", "Ctrl+V", self._plain_paste))
        em.addAction(self._act("모두 선택(&A)", "Ctrl+A", self.editor.selectAll))
        em.addSeparator()
        em.addAction(self._act("찾기(&F)...",        "Ctrl+F", self.find_bar.open_find))
        em.addAction(self._act("찾기/바꾸기(&R)...", "Ctrl+R", self.find_bar.open_replace))

        # ── 보기
        vm = mb.addMenu("보기(&V)")
        vm.addAction(self._act("확대",       "Ctrl++", self.zoom_in))
        vm.addAction(self._act("축소",       "Ctrl+-", self.zoom_out))
        vm.addAction(self._act("기본 크기로", "Ctrl+0", self.zoom_reset))
        vm.addSeparator()
        self.wrap_action = QAction("자동 줄바꿈(&W)", self, checkable=True, checked=True)
        self.wrap_action.triggered.connect(self.toggle_wrap)
        vm.addAction(self.wrap_action)

    def _build_statusbar(self):
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        self._update_status()

    # ── 액션 헬퍼 ────────────────────────────

    def _act(self, label: str, shortcut: str | None, slot) -> QAction:
        action = QAction(label, self)
        if shortcut:
            action.setShortcut(QKeySequence(shortcut))
        action.triggered.connect(slot)
        return action

    # ── 파일 작업 ────────────────────────────

    def new_file(self):
        if not self._check_save():
            return
        self.editor.clear()
        self.current_file = None
        self.setWindowTitle("cahier")
        self.editor.document().setModified(False)

    def open_file(self):
        if not self._check_save():
            return
        path, _ = QFileDialog.getOpenFileName(
            self, "열기", "",
            "텍스트 파일 (*.txt);;모든 파일 (*.*)"
        )
        if path:
            with open(path, encoding="utf-8") as f:
                self.editor.setPlainText(f.read())
            self.current_file = path
            self.setWindowTitle(f"{os.path.basename(path)} - cahier")
            self.editor.document().setModified(False)

    def open_file_path(self, path: str):
        with open(path, encoding="utf-8") as f:
            self.editor.setPlainText(f.read())
        self.current_file = path
        self.setWindowTitle(f"{os.path.basename(path)} - cahier")
        self.editor.document().setModified(False)

    def save_file(self):
        if self.current_file:
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(self.editor.toPlainText())
            self.editor.document().setModified(False)
            # 제목의 * 제거
            t = self.windowTitle()
            if t.startswith("*"):
                self.setWindowTitle(t[1:])
        else:
            self.save_as()
    
    def save_as(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "다른 이름으로 저장", "",
            "텍스트 파일 (*.txt);;모든 파일 (*.*)"
        )
        if path:
            self.current_file = path
            self.save_file()
            self.setWindowTitle(f"{os.path.basename(path)} - cahier")

    # ── 보기 ─────────────────────────────────

    def zoom_in(self):
        self.font_size += 1
        self.editor.setFont(QFont(self.font_family, self.font_size))

    def zoom_out(self):
        if self.font_size > 6:
            self.font_size -= 1
            self.editor.setFont(QFont(self.font_family, self.font_size))

    def zoom_reset(self):
        self.font_size = self.BASE_FONT_SIZE
        self.editor.setFont(QFont(self.font_family, self.font_size))

    def toggle_wrap(self):
        mode = (QTextEdit.LineWrapMode.WidgetWidth
                if self.wrap_action.isChecked()
                else QTextEdit.LineWrapMode.NoWrap)
        self.editor.setLineWrapMode(mode)

    def wheelEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.angleDelta().y() > 0:
                self.zoom_in()
            else:
                self.zoom_out()
            event.accept()
        else:
            super().wheelEvent(event)

    def eventFilter(self, obj, event):
        if obj is self.editor and event.type() == QEvent.Type.KeyPress:
            if event.matches(QKeySequence.StandardKey.Paste):
                self._plain_paste()
                return True
        return super().eventFilter(obj, event)

    def _plain_paste(self):
        clipboard = QApplication.clipboard()
        cur = self.editor.textCursor()
        cur.insertText(clipboard.text())

    # ── 내부 유틸 ─────────────────────────────

    def _on_modified(self):
        if self.editor.document().isModified():
            t = self.windowTitle()
            if not t.startswith("*"):
                self.setWindowTitle("*" + t)

    def _update_status(self):
        cur = self.editor.textCursor()
        line = cur.blockNumber() + 1
        col  = cur.columnNumber() + 1
        chars = len(self.editor.toPlainText())
        self.status_bar.showMessage(f"줄 {line}, 열 {col}   문자 수: {chars}")

    def _check_save(self) -> bool:
        """저장 확인. 계속 진행해도 되면 True 반환."""
        if not self.editor.document().isModified():
            return True
        ans = QMessageBox.question(
            self, "저장",
            "저장하지 않은 내용이 있습니다. 저장할까요?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No  |
            QMessageBox.StandardButton.Cancel,
        )
        if ans == QMessageBox.StandardButton.Yes:
            self.save_file()
            return True
        if ans == QMessageBox.StandardButton.No:
            return True
        return False  # Cancel

    def closeEvent(self, event):
        if self._check_save():
            event.accept()
        else:
            event.ignore()

app = QApplication(sys.argv)
win = Cahier()

if len(sys.argv) > 1:
    win.open_file_path(sys.argv[1])

win.show()
app.exec()