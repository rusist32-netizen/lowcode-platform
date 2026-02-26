#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Панель списка таблиц
"""

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class TableListPanel(QWidget):
    """Панель со списком таблиц проекта"""

    tableSelected = pyqtSignal(object)
    tableCreated = pyqtSignal(object)
    tableDeleted = pyqtSignal(int)

    def __init__(self, project_manager, parent=None):
        super().__init__(parent)
        self.project_manager = project_manager
        self.tables = []

        self.setup_ui()
        self.refresh()

    def setup_ui(self):
        """Создание интерфейса"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        # Кнопка создания таблицы
        create_btn = QPushButton("➕ Новая таблица")
        create_btn.setStyleSheet("""
            QPushButton {
                background-color: #0e639c;
                color: white;
                border: none;
                padding: 6px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1177bb;
            }
        """)
        create_btn.clicked.connect(self.create_table)

        layout.addWidget(create_btn)

        # Список таблиц
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("""
            QListWidget {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #4c4c4c;
                border-radius: 3px;
                padding: 4px;
            }
            QListWidget::item {
                padding: 6px;
                border-radius: 2px;
            }
            QListWidget::item:hover {
                background-color: #3c3c3c;
            }
            QListWidget::item:selected {
                background-color: #2d4f7c;
            }
        """)
        self.list_widget.itemClicked.connect(self.on_item_clicked)

        layout.addWidget(self.list_widget, 1)

    def refresh(self):
        """Обновляет список таблиц"""
        self.list_widget.clear()
        self.tables = self.project_manager.get_all_tables()

        for table in self.tables:
            icon = table.get('icon', '📊')
            name = table.get('display_name', 'Без имени')
            protected = table.get('protected', False)

            text = f"{icon} {name}"
            if protected:
                text = "🔒 " + text

            item = QListWidgetItem(text)
            item.setData(Qt.ItemDataRole.UserRole, table)
            self.list_widget.addItem(item)

    def create_table(self):
        """Создаёт новую таблицу"""
        name, ok = QInputDialog.getText(self, "Новая таблица", "Введите название таблицы:")
        if ok and name.strip():
            table_data = self.project_manager.create_table(name.strip())
            self.refresh()
            self.tableCreated.emit(table_data)

    def on_item_clicked(self, item):
        """Обработка клика по таблице"""
        table_data = item.data(Qt.ItemDataRole.UserRole)
        self.tableSelected.emit(table_data)