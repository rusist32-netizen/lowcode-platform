#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Виджет поля в конструкторе таблиц
"""

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class FieldWidget(QFrame):
    """Виджет для отображения поля в конструкторе"""

    fieldClicked = pyqtSignal(object)
    fieldMoved = pyqtSignal(int, int)
    fieldDeleted = pyqtSignal(object)

    def __init__(self, field_data, parent=None):
        super().__init__(parent)
        self.field_data = field_data
        self.is_selected = False
        self.drag_start_position = None

        self.setup_ui()
        self.update_display(field_data)

    def setup_ui(self):
        """Создание интерфейса"""
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setCursor(Qt.CursorShape.OpenHandCursor)
        self.setAcceptDrops(True)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(6)

        # Ручка для перетаскивания
        self.drag_handle = QLabel("⋮⋮")
        self.drag_handle.setCursor(Qt.CursorShape.SizeAllCursor)
        self.drag_handle.setStyleSheet("color: #888; font-size: 14px;")

        # Иконка типа поля
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(20, 20)

        # Название поля
        self.name_label = QLabel()
        self.name_label.setStyleSheet("color: #9cdcfe; font-weight: bold;")

        # Тип поля
        self.type_label = QLabel()
        self.type_label.setStyleSheet("color: #888; font-size: 11px;")

        # Кнопка удаления
        self.delete_btn = QPushButton("✕")
        self.delete_btn.setFixedSize(20, 20)
        self.delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #888;
                border: none;
                font-size: 12px;
            }
            QPushButton:hover {
                color: #f14c4c;
            }
        """)
        self.delete_btn.clicked.connect(self.on_delete)

        layout.addWidget(self.drag_handle)
        layout.addWidget(self.icon_label)
        layout.addWidget(self.name_label, 1)
        layout.addWidget(self.type_label)
        layout.addWidget(self.delete_btn)

    def update_display(self, field_data):
        """Обновляет отображение поля"""
        self.field_data = field_data

        # Иконка в зависимости от типа
        type_icons = {
            'TEXT': '📝',
            'TEXT_MULTILINE': '📄',
            'INTEGER': '🔢',
            'FLOAT': '🔢',
            'DATE': '📅',
            'TIME': '⏰',
            'DATETIME': '📆',
            'BOOLEAN': '✅',
            'LIST': '📋',
            'REFERENCE': '🔗',
            'PHONE': '📞',
            'EMAIL': '✉️',
            'MONEY': '💰',
            'PERCENT': '📊',
            'FILE': '📎',
            'IMAGE': '🖼️',
            'COLOR': '🎨',
            'RATING': '⭐',
            'CALCULATED': '🧮',
        }

        field_type = field_data.get('type', 'TEXT')
        if hasattr(field_type, 'value'):
            field_type = field_type.value

        icon = type_icons.get(field_type, '📌')
        self.icon_label.setText(icon)

        # Название
        self.name_label.setText(field_data.get('display_name', 'Поле'))

        # Тип для отображения
        type_names = {
            'TEXT': 'Текст',
            'TEXT_MULTILINE': 'Многостр.',
            'INTEGER': 'Целое',
            'FLOAT': 'Дробное',
            'DATE': 'Дата',
            'TIME': 'Время',
            'DATETIME': 'Дата/время',
            'BOOLEAN': 'Да/Нет',
            'LIST': 'Список',
            'REFERENCE': 'Ссылка',
            'PHONE': 'Тел.',
            'EMAIL': 'Email',
            'MONEY': 'Деньги',
            'PERCENT': '%',
            'FILE': 'Файл',
            'IMAGE': 'Изобр.',
            'COLOR': 'Цвет',
            'RATING': 'Рейтинг',
            'CALCULATED': 'Вычисл.',
        }
        self.type_label.setText(type_names.get(field_type, field_type))

        # Обязательное поле - добавляем звёздочку
        if field_data.get('required'):
            self.name_label.setText(self.name_label.text() + " *")
            self.name_label.setStyleSheet("color: #f4a261; font-weight: bold;")

    def set_selected(self, selected):
        """Устанавливает выделение поля"""
        self.is_selected = selected
        if selected:
            self.setStyleSheet("""
                QFrame {
                    background-color: #2d4f7c;
                    border: 1px solid #4c9cdc;
                    border-radius: 4px;
                }
            """)
        else:
            self.setStyleSheet("""
                QFrame {
                    background-color: #2d2d2d;
                    border: 1px solid #3c3c3c;
                    border-radius: 4px;
                }
                QFrame:hover {
                    background-color: #3c3c3c;
                }
            """)

    def on_delete(self):
        """Обработка удаления"""
        self.fieldDeleted.emit(self.field_data)

    # ===== МЕТОДЫ ДЛЯ DRAG & DROP =====

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = event.pos()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            self.fieldClicked.emit(self.field_data)

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.MouseButton.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return

        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText("field")
        drag.setMimeData(mime_data)

        pixmap = self.grab()
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())

        self.setCursor(Qt.CursorShape.OpenHandCursor)
        drag.exec(Qt.DropAction.MoveAction)

    def mouseReleaseEvent(self, event):
        self.setCursor(Qt.CursorShape.OpenHandCursor)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText() and event.mimeData().text() == "field":
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasText() and event.mimeData().text() == "field":
            source_widget = event.source()
            if source_widget and isinstance(source_widget, FieldWidget):
                parent_layout = self.parentWidget().layout()
                if parent_layout:
                    source_index = parent_layout.indexOf(source_widget)
                    target_index = parent_layout.indexOf(self)

                    if source_index < target_index:
                        parent_layout.insertWidget(target_index, source_widget)
                    else:
                        parent_layout.insertWidget(target_index + 1, source_widget)

                    event.acceptProposedAction()