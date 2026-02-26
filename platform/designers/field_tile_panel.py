# -*- coding: utf-8 -*-

"""
Правая панель с плитками типов полей
"""

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from platform.core.field_types import FieldType
from platform.widgets.field_tile import FieldTile


class FieldTilePanel(QWidget):
    """Правая панель с плитками типов полей"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setFixedWidth(200)
        self.setStyleSheet("""
            QWidget {
                background-color: #0f172a;
                border-left: 1px solid #334155;
            }
        """)
        
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        
        title = QLabel("🔧 ТИПЫ ПОЛЕЙ")
        title.setStyleSheet("color: #3b82f6; font-size: 12px; font-weight: bold;")
        layout.addWidget(title)
        
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
        
        tiles_widget = QWidget()
        tiles_layout = QGridLayout(tiles_widget)
        tiles_layout.setContentsMargins(0, 0, 0, 0)
        tiles_layout.setSpacing(4)
        
        for i, (icon, name, desc, type_id) in enumerate(FieldType.TYPES):
            tile = FieldTile(icon, name, desc, type_id)
            tiles_layout.addWidget(tile, i // 2, i % 2)
        
        scroll.setWidget(tiles_widget)
        layout.addWidget(scroll)