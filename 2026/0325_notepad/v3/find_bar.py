from PyQt6.QtWidgets import (
    QWidget, QTextEdit, QHBoxLayout, QLineEdit,
    QPushButton, QLabel, QVBoxLayout,
)
from PyQt6.QtGui import QColor, QTextCursor
from PyQt6.QtCore import Qt


class FindBar(QWidget):
    def __init__(self, editor: QTextEdit, parent=None):
        super().__init__(parent)
        self.editor = editor
        self._matches: list[int] = []
        self._current = -1

        self._build_ui()
        self.hide()

    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(8, 6, 8, 6)
        outer.setSpacing(4)

        # ── 찾기 행
        find_row = QHBoxLayout()
        find_row.setSpacing(4)
        self.find_edit = QLineEdit()
        self.find_edit.setPlaceholderText("찾기")
        self.count_label = QLabel("")
        prev_btn = QPushButton("▲")
        next_btn = QPushButton("▼")
        close_btn = QPushButton("✕")
        close_btn.setFixedWidth(28)
        find_row.addWidget(self.find_edit)
        find_row.addWidget(prev_btn)
        find_row.addWidget(next_btn)
        find_row.addWidget(self.count_label)
        find_row.addStretch()
        find_row.addWidget(close_btn)
        outer.addLayout(find_row)

        # ── 바꾸기 행
        self.rep_row_widget = QWidget()
        rep_row = QHBoxLayout(self.rep_row_widget)
        rep_row.setContentsMargins(0, 0, 0, 0)
        rep_row.setSpacing(4)
        self.rep_edit = QLineEdit()
        self.rep_edit.setPlaceholderText("바꾸기")
        rep_btn = QPushButton("바꾸기")
        rep_all_btn = QPushButton("모두 바꾸기")
        rep_row.addWidget(self.rep_edit)
        rep_row.addWidget(rep_btn)
        rep_row.addWidget(rep_all_btn)
        rep_row.addStretch()
        outer.addWidget(self.rep_row_widget)

        # 시그널 연결
        self.find_edit.textChanged.connect(self._on_text_changed)
        self.find_edit.returnPressed.connect(self.find_next)
        next_btn.clicked.connect(self.find_next)
        prev_btn.clicked.connect(self.find_prev)
        close_btn.clicked.connect(self.close_bar)
        rep_btn.clicked.connect(self.do_replace)
        rep_all_btn.clicked.connect(self.do_replace_all)

    # ── 열기 ──────────────────────────────────

    def open_find(self):
        self.rep_row_widget.hide()
        self.setFixedHeight(40)
        self.show()
        self.find_edit.setFocus()
        self.find_edit.selectAll()

    def open_replace(self):
        self.rep_row_widget.show()
        self.setFixedHeight(72)
        self.show()
        self.find_edit.setFocus()
        self.find_edit.selectAll()

    def close_bar(self):
        self._clear_highlights()
        self.hide()
        self.editor.setFocus()

    # ── 검색 로직 ─────────────────────────────

    def _on_text_changed(self):
        self._highlight_all(self.find_edit.text())

    def _highlight_all(self, keyword: str):
        self._clear_highlights()
        self._matches.clear()
        self._current = -1

        if not keyword:
            self.count_label.setText("")
            return

        doc = self.editor.document()
        extras = []
        cursor = doc.find(keyword)
        while not cursor.isNull():
            sel = QTextEdit.ExtraSelection()
            sel.cursor = cursor
            sel.format.setBackground(QColor("#7a6a00"))
            extras.append(sel)
            self._matches.append(cursor.selectionStart())
            cursor = doc.find(keyword, cursor)

        self.editor.setExtraSelections(extras)

        if self._matches:
            self._current = 0
            self._go_to(0, keyword)
        else:
            self.count_label.setText("없음")

    def _go_to(self, idx: int, keyword: str):
        self._current = idx
        pos = self._matches[idx]

        extras = self.editor.extraSelections()
        for sel in extras:
            if sel.cursor.selectionStart() == pos:
                sel.format.setBackground(QColor("#c8a000"))
            else:
                sel.format.setBackground(QColor("#7a6a00"))
        self.editor.setExtraSelections(extras)

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
        if not self._matches:
            self._highlight_all(keyword)
            return
        self._current = (self._current + 1) % len(self._matches)
        self._go_to(self._current, keyword)

    def find_prev(self):
        keyword = self.find_edit.text()
        if not keyword or not self._matches:
            return
        self._current = (self._current - 1) % len(self._matches)
        self._go_to(self._current, keyword)

    def _clear_highlights(self):
        self.editor.setExtraSelections([])

    # ── 바꾸기 ────────────────────────────────

    def do_replace(self):
        keyword = self.find_edit.text()
        if not self._matches or not keyword:
            return
        pos = self._matches[self._current]
        cur = self.editor.textCursor()
        cur.setPosition(pos)
        cur.setPosition(pos + len(keyword), QTextCursor.MoveMode.KeepAnchor)
        cur.insertText(self.rep_edit.text())
        self._highlight_all(keyword)

    def do_replace_all(self):
        keyword = self.find_edit.text()
        if not keyword:
            return
        text = self.editor.toPlainText()
        count = text.count(keyword)
        if count == 0:
            self.count_label.setText("없음")
            return
        new_text = text.replace(keyword, self.rep_edit.text())
        self.editor.setPlainText(new_text)
        self.count_label.setText(f"{count}개 바꿈")

    # ── 키 이벤트 ─────────────────────────────

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close_bar()
        elif event.key() == Qt.Key.Key_Return and event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
            self.find_prev()
        else:
            super().keyPressEvent(event)