#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Просмотр таблицы (данные)
"""

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class TableViewer(QWidget):
    """
    Компонент для просмотра данных таблицы
    """

    recordAdded = pyqtSignal(dict)
    recordEdited = pyqtSignal(dict)
    recordDeleted = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_table = None
        self.table_data = []
        self.setup_ui()

    def setup_ui(self):
        """Создание интерфейса просмотра"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Панель инструментов
        toolbar = QWidget()
        toolbar.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                border-bottom: 1px solid #3c3c3c;
            }
        """)
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(8, 4, 8, 4)

        self.add_btn = QPushButton("➕ Добавить")
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #0e639c;
                color: white;
                border: none;
                padding: 4px 8px;
                border-radius: 3px;
                font-size: 12px;
            }
            QPushButton:hover { background-color: #1177bb; }
        """)
        self.add_btn.clicked.connect(self.add_record)

        self.edit_btn = QPushButton("✏️ Редактировать")
        self.edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #4c4c4c;
                color: white;
                border: none;
                padding: 4px 8px;
                border-radius: 3px;
                font-size: 12px;
            }
            QPushButton:hover { background-color: #5c5c5c; }
            QPushButton:disabled { background-color: #2d2d2d; color: #888; }
        """)
        self.edit_btn.setEnabled(False)
        self.edit_btn.clicked.connect(self.edit_record)

        self.delete_btn = QPushButton("🗑️ Удалить")
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #a1260d;
                color: white;
                border: none;
                padding: 4px 8px;
                border-radius: 3px;
                font-size: 12px;
            }
            QPushButton:hover { background-color: #c42b1c; }
            QPushButton:disabled { background-color: #2d2d2d; color: #888; }
        """)
        self.delete_btn.setEnabled(False)
        self.delete_btn.clicked.connect(self.delete_record)

        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("🔍 Поиск...")
        self.search_edit.setStyleSheet("""
            QLineEdit {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #4c4c4c;
                border-radius: 3px;
                padding: 4px 8px;
                font-size: 12px;
                min-width: 200px;
            }
        """)
        self.search_edit.textChanged.connect(self.filter_table)

        toolbar_layout.addWidget(self.add_btn)
        toolbar_layout.addWidget(self.edit_btn)
        toolbar_layout.addWidget(self.delete_btn)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.search_edit)

        layout.addWidget(toolbar)

        # Таблица с данными
        self.table = QTableWidget()
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #1e1e1e;
                color: #e0e0e0;
                gridline-color: #3c3c3c;
                border: none;
            }
            QTableWidget::item {
                padding: 4px;
            }
            QTableWidget::item:selected {
                background-color: #2d4f7c;
            }
            QHeaderView::section {
                background-color: #2d2d2d;
                color: #9cdcfe;
                padding: 6px;
                border: 1px solid #3c3c3c;
                font-weight: bold;
                font-size: 12px;
            }
        """)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.itemSelectionChanged.connect(self.on_selection_changed)

        layout.addWidget(self.table, 1)

        # Строка статуса
        status_bar = QWidget()
        status_bar.setStyleSheet("background-color: #1e1e1e; border-top: 1px solid #3c3c3c;")
        status_layout = QHBoxLayout(status_bar)
        status_layout.setContentsMargins(8, 4, 8, 4)

        self.status_label = QLabel("Нет данных")
        self.status_label.setStyleSheet("color: #888; font-size: 11px;")

        status_layout.addWidget(self.status_label)

        layout.addWidget(status_bar)

    def set_table(self, table_definition, data=None):
        """Устанавливает таблицу для отображения"""
        self.current_table = table_definition
        self.table_data = data or []

        fields = table_definition.get('fields', [])
        self.table.setColumnCount(len(fields))
        headers = [f.get('display_name', f.get('name', '')) for f in fields]
        self.table.setHorizontalHeaderLabels(headers)

        self.refresh_table()

    def refresh_table(self):
        """Обновляет отображение таблицы"""
        self.table.setRowCount(0)

        if not self.table_data:
            self.status_label.setText("Нет данных")
            return

        fields = self.current_table.get('fields', [])

        for row, record in enumerate(self.table_data):
            self.table.insertRow(row)

            for col, field in enumerate(fields):
                field_name = field.get('name')
                value = record.get(field_name, '')
                item = QTableWidgetItem(str(value))
                item.setData(Qt.ItemDataRole.UserRole, record)
                self.table.setItem(row, col, item)

        self.status_label.setText(f"Записей: {len(self.table_data)}")

    def add_record(self):
        """Добавление новой записи"""
        QMessageBox.information(self, "Добавление", "Здесь будет форма добавления записи")

    def edit_record(self):
        """Редактирование выбранной записи"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            QMessageBox.information(self, "Редактирование", f"Редактирование записи {current_row + 1}")

    def delete_record(self):
        """Удаление выбранной записи"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            reply = QMessageBox.question(
                self, "Подтверждение",
                f"Удалить запись №{current_row + 1}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.table.removeRow(current_row)

    def filter_table(self, text):
        """Фильтрация таблицы по тексту"""
        for row in range(self.table.rowCount()):
            visible = False
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and text.lower() in item.text().lower():
                    visible = True
                    break
            self.table.setRowHidden(row, not visible)

    def on_selection_changed(self):
        """Обработка изменения выделения"""
        has_selection = len(self.table.selectedIndexes()) > 0
        self.edit_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)

    def on_field_selected(self, field_data):
        """Вызывается при выборе поля в конструкторе"""
        pass