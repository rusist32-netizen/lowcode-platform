# -*- coding: utf-8 -*-

"""
Элемент списка таблиц
"""

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class TableItem(QWidget):
    """Элемент списка таблиц"""
    
    clicked = pyqtSignal(object)
    renameRequested = pyqtSignal(object)
    
    def __init__(self, table_data: dict, parent=None):
        super().__init__(parent)
        
        self.table_data = table_data
        
        self.setFixedHeight(32)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 2, 8, 2)
        layout.setSpacing(4)
        
        icon = QLabel(self.table_data.get('icon', '📊'))
        icon.setStyleSheet("font-size: 16px;")
        icon.setFixedSize(20, 20)
        layout.addWidget(icon)
        
        name = QLabel(self.table_data['name_ru'])
        name.setStyleSheet("color: #e2e8f0; font-weight: 500; font-size: 12px;")
        layout.addWidget(name, 1)
        
        self.active_indicator = QLabel()
        self.active_indicator.setFixedSize(6, 6)
        self.active_indicator.setStyleSheet("background-color: transparent; border-radius: 3px;")
        layout.addWidget(self.active_indicator)
        
        rename_btn = QPushButton("✏️")
        rename_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        rename_btn.setFixedSize(18, 18)
        rename_btn.setToolTip("Переименовать")
        rename_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #f59e0b;
                border: none;
                border-radius: 3px;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #f59e0b;
                color: white;
            }
        """)
        rename_btn.clicked.connect(lambda: self.renameRequested.emit(self.table_data))
        layout.addWidget(rename_btn)
        
        self.setStyleSheet("""
            TableItem {
                background-color: transparent;
                border: none;
                border-radius: 4px;
            }
            TableItem:hover {
                background-color: #2d3a4f;
            }
        """)
    
    def set_active(self, active: bool):
        if active:
            self.active_indicator.setStyleSheet("background-color: #3b82f6; border-radius: 3px;")
            self.setStyleSheet("""
                TableItem {
                    background-color: #2d3a4f;
                    border: none;
                    border-radius: 4px;
                }
            """)
        else:
            self.active_indicator.setStyleSheet("background-color: transparent; border-radius: 3px;")
            self.setStyleSheet("""
                TableItem {
                    background-color: transparent;
                    border: none;
                    border-radius: 4px;
                }
                TableItem:hover {
                    background-color: #2d3a4f;
                }
            """)
    
    def mousePressEvent(self, event):
        self.clicked.emit(self.table_data)
        super().mousePressEvent(event)