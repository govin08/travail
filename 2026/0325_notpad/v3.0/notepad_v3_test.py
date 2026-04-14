import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit
from PyQt6.QtGui import QAction, QKeySequence

class Notepad(QMainWindow):
    def __init__(self):
        super().__init__()
        self.editor = QTextEdit(self)
        self.setCentralWidget(self.editor)
        self._build_menu()
        self.resize(400, 300)

    def _build_menu(self):
        mb = self.menuBar()

        fm = mb.addMenu("파일")
        fm.addAction(self._act("새로 만들기", "Ctrl+N", lambda: None))
        fm.addAction(self._act("열기",        "Ctrl+O", lambda: None))

        em = mb.addMenu("편집")
        em.addAction(self._act("복사", "Ctrl+C", self.editor.copy))

        vm = mb.addMenu("보기")
        vm.addAction(self._act("확대", "Ctrl++", lambda: None))

    def _act(self, label, shortcut, slot):  # @staticmethod 제거, self 하나만
        action = QAction(label, self)       # parent=self 추가
        if shortcut:
            action.setShortcut(QKeySequence(shortcut))
        action.triggered.connect(slot)
        return action

app = QApplication(sys.argv)
win = Notepad()
win.show()
sys.exit(app.exec())