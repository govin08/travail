# v2 : Ctrl+F 기능 추가, Ctrl+H -> Ctrl+R
# v2.1 : 서식 -> 보기, 글꼴항목 없애기, 확대 및 축소 기능
# - 파일 작업 / 편집 / 찾기·바꾸기 / 보기(확대축소·자동줄바꿈)
# - 한글 IME 완전 지원 (QTextEdit 기반)
# - 상태표시줄 (줄·열·문자수)
# v3.0 : PyQt6 사용 (기존 : tkinter)

import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit,
    QFileDialog, QMessageBox, QStatusBar,
    QDialog, QLabel, QLineEdit, QPushButton,
    QGridLayout,
)
from PyQt6.QtGui import (
    QAction, QKeySequence, QFont, QTextCursor,
)
from PyQt6.QtCore import Qt


# ──────────────────────────────────────────────
# 찾기 다이얼로그
# ──────────────────────────────────────────────
class FindDialog(QDialog):
    def __init__(self, editor: QTextEdit, parent=None):
        super().__init__(parent)
        self.editor = editor
        self.setWindowTitle("찾기")
        self.setFixedSize(360, 110)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

        self.find_edit = QLineEdit()
        self.count_label = QLabel("")
        self.count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        find_btn = QPushButton("찾기")

        layout = QGridLayout(self)
        layout.addWidget(QLabel("찾기:"),      0, 0)
        layout.addWidget(self.find_edit,        0, 1)
        layout.addWidget(find_btn,              0, 2)
        layout.addWidget(self.count_label,      1, 0, 1, 3)

        find_btn.clicked.connect(self.find_next)
        self.find_edit.returnPressed.connect(self.find_next)

        self._matches: list[int] = []   # 각 매치의 시작 위치(절대)
        self._current = -1

    # 하이라이트 전체 갱신
    def _highlight_all(self, keyword: str):
        doc = self.editor.document()
        self._matches.clear()

        from PyQt6.QtGui import QColor
        extras = []
        cursor = doc.find(keyword)
        while not cursor.isNull():
            sel = QTextEdit.ExtraSelection()
            sel.cursor = cursor
            sel.format.setBackground(QColor("yellow"))
            extras.append(sel)
            self._matches.append(cursor.selectionStart())
            cursor = doc.find(keyword, cursor)

        self.editor.setExtraSelections(extras)

    def _go_to(self, idx: int, keyword: str):
        from PyQt6.QtGui import QColor

        self._current = idx
        pos = self._matches[idx]

        # 현재 매치는 주황색
        extras = self.editor.extraSelections()
        for sel in extras:
            if sel.cursor.selectionStart() == pos:
                sel.format.setBackground(QColor("orange"))
            else:
                sel.format.setBackground(QColor("yellow"))
        self.editor.setExtraSelections(extras)

        # 커서 이동
        cur = self.editor.textCursor()
        cur.setPosition(pos)
        cur.setPosition(pos + len(keyword), QTextCursor.MoveMode.KeepAnchor)
        self.editor.setTextCursor(cur)
        self.editor.ensureCursorVisible()
        self.count_label.setText(f"{idx + 1} / {len(self._matches)}")

    def find_next(self):
        keyword = self.find_edit.text()
        if not keyword:
            return
        self._highlight_all(keyword)
        if not self._matches:
            self.count_label.setText("없음")
            return
        self._current = (self._current + 1) % len(self._matches)
        self._go_to(self._current, keyword)

    def closeEvent(self, event):
        self.editor.setExtraSelections([])
        super().closeEvent(event)


# ──────────────────────────────────────────────
# 찾기/바꾸기 다이얼로그
# ──────────────────────────────────────────────
class FindReplaceDialog(FindDialog):
    def __init__(self, editor: QTextEdit, parent=None):
        super().__init__(editor, parent)
        self.setWindowTitle("찾기/바꾸기")
        self.setFixedSize(360, 150)

        self.rep_edit = QLineEdit()
        rep_btn = QPushButton("바꾸기")

        layout: QGridLayout = self.layout()
        layout.addWidget(QLabel("바꾸기:"), 2, 0)
        layout.addWidget(self.rep_edit,      2, 1)
        layout.addWidget(rep_btn,            2, 2)

        rep_btn.clicked.connect(self.do_replace)

    def do_replace(self):
        keyword = self.find_edit.text()
        if not self._matches:
            self.find_next()
            return
        pos = self._matches[self._current]
        cur = self.editor.textCursor()
        cur.setPosition(pos)
        cur.setPosition(pos + len(keyword), QTextCursor.MoveMode.KeepAnchor)
        cur.insertText(self.rep_edit.text())
        self.find_next()


# ──────────────────────────────────────────────
# 메인 윈도우
# ──────────────────────────────────────────────
class Notepad(QMainWindow):
    BASE_FONT_SIZE = 11

    def __init__(self):
        super().__init__()
        self.current_file: str | None = None
        self.font_family = "맑은 고딕"
        self.font_size = self.BASE_FONT_SIZE

        self._build_editor()
        self._build_menu()
        self._build_statusbar()

        self.setWindowTitle("메모장")
        self.resize(800, 600)

    # ── UI 구성 ──────────────────────────────

    def _build_editor(self):
        self.editor = QTextEdit(self)
        self.editor.setFont(QFont(self.font_family, self.font_size))
        self.editor.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        self.setCentralWidget(self.editor)

        self.editor.document().contentsChanged.connect(self._on_modified)
        self.editor.cursorPositionChanged.connect(self._update_status)

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
        em.addAction(self._act("붙여넣기(&P)", "Ctrl+V", self.editor.paste))
        em.addAction(self._act("모두 선택(&A)", "Ctrl+A", self.editor.selectAll))
        em.addSeparator()
        em.addAction(self._act("찾기(&F)...",        "Ctrl+F", self.show_find))
        em.addAction(self._act("찾기/바꾸기(&R)...", "Ctrl+R", self.show_find_replace))

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
        self.setWindowTitle("메모장")
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
            self.setWindowTitle(f"{os.path.basename(path)} - 메모장")
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
            self.setWindowTitle(f"{os.path.basename(path)} - 메모장")

    # ── 찾기 / 바꾸기 ────────────────────────

    def show_find(self):
        dlg = FindDialog(self.editor, self)
        dlg.show()

    def show_find_replace(self):
        dlg = FindReplaceDialog(self.editor, self)
        dlg.show()

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


# ──────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = Notepad()
    win.show()
    sys.exit(app.exec())
