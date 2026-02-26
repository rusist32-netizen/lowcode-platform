# -*- coding: utf-8 -*-

"""
Левая панель со списком таблиц
"""

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from typing import Optional

from platform.core.translator import Translator
from platform.widgets.table_item import TableItem


class TableListPanel(QWidget):
    """Левая панель со списком таблиц"""
    
    tableSelected = pyqtSignal(dict)
    tableCreated = pyqtSignal()
    tableRenamed = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.tables = []
        
        self.setFixedWidth(200)
        self.setStyleSheet("""
            QWidget {
                background-color: #0f172a;
                border-right: 1px solid #334155;
            }
        """)
        
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        
        title = QLabel("📊 ТАБЛИЦЫ")
        title.setStyleSheet("color: #3b82f6; font-size: 12px; font-weight: bold;")
        layout.addWidget(title)
        
        create_btn = QPushButton("➕ Создать таблицу")
        create_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        create_btn.setFixedHeight(26)
        create_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: white;
                border: none;
                border-radius: 3px;
                font-weight: 500;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
            QPushButton:disabled {
                background-color: #475569;
                color: #94a3b8;
            }
        """)
        create_btn.clicked.connect(self._create_table)
        layout.addWidget(create_btn)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background-color: #1e293b;
                width: 6px;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical {
                background-color: #475569;
                border-radius: 3px;
                min-height: 20px;
            }
        """)
        
        self.list_widget = QWidget()
        self.list_layout = QVBoxLayout(self.list_widget)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(2)
        self.list_layout.addStretch()
        
        scroll.setWidget(self.list_widget)
        layout.addWidget(scroll)
    
    def _create_table(self):
        name, ok = QInputDialog.getText(
            self, 
            "Новая таблица", 
            "Введите название таблицы:"
        )
        
        if ok and name.strip():
            table_id = f"table_{len(self.tables)}_{Translator.to_english(name)}"
            table = {
                'id': table_id,
                'name_ru': name.strip(),
                'name_en': Translator.to_english(name.strip()),
                'icon': '📊',
                'fields': [],
                'references': [],
                'referenced_by': []
            }
            
            self.add_table(table)
            self.tableCreated.emit()
    
    def add_table(self, table_data: dict):
        self.tables.append(table_data)
        
        item = TableItem(table_data)
        item.clicked.connect(self._select_table)
        item.renameRequested.connect(self._rename_table)
        
        self.list_layout.insertWidget(self.list_layout.count() - 1, item)
        
        if len(self.tables) == 1:
            self._select_table(table_data)
    
    def _select_table(self, table_data: dict):
        for i in range(self.list_layout.count()):
            item = self.list_layout.itemAt(i)
            if item and item.widget() and isinstance(item.widget(), TableItem):
                item.widget().set_active(item.widget().table_data['id'] == table_data['id'])
        
        self.tableSelected.emit(table_data)
    
    def _rename_table(self, table_data: dict):
        name, ok = QInputDialog.getText(
            self,
            "Переименовать таблицу",
            "Введите новое название:",
            text=table_data['name_ru']
        )
        
        if ok and name.strip() and name != table_data['name_ru']:
            table_data['name_ru'] = name.strip()
            table_data['name_en'] = Translator.to_english(name.strip())
            self.update_table(table_data)
            self.tableRenamed.emit(table_data)
    
    def update_table(self, table_data: dict):
        for i in range(self.list_layout.count()):
            item = self.list_layout.itemAt(i)
            if item and item.widget() and isinstance(item.widget(), TableItem):
                if item.widget().table_data['id'] == table_data['id']:
                    self.list_layout.removeWidget(item.widget())
                    item.widget().deleteLater()
                    
                    new_item = TableItem(table_data)
                    new_item.clicked.connect(self._select_table)
                    new_item.renameRequested.connect(self._rename_table)
                    
                    self.list_layout.insertWidget(i, new_item)
                    break
    
    def get_tables(self) -> list:
        return self.tables.copy()
    
    def setEnabled(self, enabled: bool):
        """Переопределяем для блокировки всех элементов"""
        super().setEnabled(enabled)
        for i in range(self.list_layout.count()):
            item = self.list_layout.itemAt(i)
            if item and item.widget():
                item.widget().setEnabled(enabled)