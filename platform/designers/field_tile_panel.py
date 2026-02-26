#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Панель с плитками полей
"""

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class FieldTile(QPushButton):
    """Плитка поля для перетаскивания"""

    def __init__(self, field_type, icon, label, parent=None):
        super().__init__(parent)
        self.field_type = field_type
        self.setAcceptDrops(False)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(2)

        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("font-size: 20px;")

        text_label = QLabel(label)
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_label.setStyleSheet("font-size: 11px; color: #e0e0e0;")

        layout.addWidget(icon_label)
        layout.addWidget(text_label)

        self.setFixedSize(70, 70)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background-color: #2d2d2d;
                border: 1px solid #4c4c4c;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #3c3c3c;
                border: 1px solid #0e639c;
            }
        """)


class FieldTilePanel(QWidget):
    """Панель с плитками полей"""

    fieldTileClicked = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        """Создание интерфейса"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        # Заголовок
        title = QLabel("ПЕРЕТАЩИТЕ ПОЛЕ")
        title.setStyleSheet("""
            QLabel {
                color: #4ec9b0;
                font-weight: bold;
                font-size: 11px;
                padding: 2px;
            }
        """)
        layout.addWidget(title)

        # Сетка с плитками
        grid = QWidget()
        grid_layout = QGridLayout(grid)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.setSpacing(4)

        # Все типы полей
        fields = [
            ("TEXT", "📝", "Текст"),
            ("TEXT_MULTILINE", "📄", "Многостр."),
            ("INTEGER", "🔢", "Число"),
            ("FLOAT", "🔢", "Дробное"),
            ("DATE", "📅", "Дата"),
            ("TIME", "⏰", "Время"),
            ("DATETIME", "📆", "Дата/время"),
            ("BOOLEAN", "✅", "Да/Нет"),
            ("LIST", "📋", "Список"),
            ("REFERENCE", "🔗", "Ссылка"),
            ("PHONE", "📞", "Телефон"),
            ("EMAIL", "✉️", "Email"),
            ("MONEY", "💰", "Деньги"),
            ("PERCENT", "📊", "Процент"),
            ("FILE", "📎", "Файл"),
            ("IMAGE", "🖼️", "Изобр."),
            ("COLOR", "🎨", "Цвет"),
            ("RATING", "⭐", "Рейтинг"),
            ("CALCULATED", "🧮", "Вычисл."),
        ]

        row, col = 0, 0
        for field_type, icon, label in fields:
            tile = FieldTile(field_type, icon, label)
            tile.clicked.connect(lambda checked, ft=field_type: self.fieldTileClicked.emit(ft))
            grid_layout.addWidget(tile, row, col)

            col += 1
            if col > 3:
                col = 0
                row += 1

        layout.addWidget(grid)