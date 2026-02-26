# -*- coding: utf-8 -*-

"""
Строка поля с кнопками управления - ПОЛНОСТЬЮ ИГНОРИРУЕТ DROP
"""

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from platform.core.translator import Translator
from platform.core.field_types import FieldType


class FieldRow(QWidget):
    """Строка поля в таблице"""
    
    movedUp = pyqtSignal(object)
    movedDown = pyqtSignal(object)
    removed = pyqtSignal(object)
    selected = pyqtSignal(object)
    
    def __init__(self, field_data: dict, index: int, tables_list=None, parent=None):
        super().__init__(parent)
        
        self.field_data = field_data
        self.index = index
        self.tables_list = tables_list or []
        
        self.setFixedHeight(32)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # КРИТИЧЕСКИ ВАЖНО: запрещаем этой строке принимать Drop
        self.setAcceptDrops(False)
        
        self.setStyleSheet("""
            FieldRow {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 4px;
                margin: 0px;
                padding: 0px;
            }
            FieldRow:hover {
                border: 2px solid #3b82f6;
            }
            FieldRow[selected="true"] {
                border: 2px solid #3b82f6;
                background-color: #2d3a4f;
            }
            FieldRow:disabled {
                background-color: #0f172a;
                border: 1px solid #1e293b;
                color: #475569;
            }
            FieldRow:disabled QLineEdit {
                background-color: #0f172a;
                color: #475569;
                border: 1px solid #1e293b;
            }
            FieldRow:disabled QPushButton {
                color: #475569;
            }
        """)
        
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 2, 6, 2)
        layout.setSpacing(4)
        
        self.num_label = QLabel(f"{self.index + 1}.")
        self.num_label.setFixedWidth(25)
        self.num_label.setStyleSheet("color: #64748b; font-size: 12px; font-weight: bold;")
        self.num_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.num_label)
        
        icon = FieldType.get_icon(self.field_data['type'])
        self.icon_label = QLabel(icon)
        self.icon_label.setFixedSize(20, 20)
        self.icon_label.setStyleSheet("font-size: 16px; background-color: transparent;")
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.icon_label)
        
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Имя поля")
        self.name_edit.setText(self.field_data.get('name_ru', ''))
        self.name_edit.setFixedHeight(24)
        self.name_edit.setStyleSheet("""
            QLineEdit {
                background-color: #0f172a;
                color: #e2e8f0;
                border: 1px solid #334155;
                border-radius: 3px;
                padding: 2px 6px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 1px solid #3b82f6;
            }
            QLineEdit:disabled {
                background-color: #0f172a;
                color: #475569;
                border: 1px solid #1e293b;
            }
        """)
        self.name_edit.textChanged.connect(self._on_name_changed)
        layout.addWidget(self.name_edit, 1)
        
        if FieldType.is_reference(self.field_data['type']):
            ref_label = QLabel("🔗")
            ref_label.setFixedSize(18, 18)
            ref_label.setStyleSheet("font-size: 12px;")
            ref_label.setToolTip("Связанное поле")
            layout.addWidget(ref_label)
        
        self.required_label = QLabel()
        self.required_label.setFixedSize(18, 18)
        self._update_indicators()
        layout.addWidget(self.required_label)
        
        btn_style = """
            QPushButton {
                background-color: transparent;
                color: #94a3b8;
                border: none;
                border-radius: 3px;
                font-size: 11px;
                padding: 0px;
                margin: 0px;
            }
            QPushButton:hover {
                background-color: #3b82f6;
                color: white;
            }
            QPushButton:disabled {
                color: #475569;
            }
        """
        
        self.up_btn = QPushButton("▲")
        self.up_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.up_btn.setFixedSize(20, 20)
        self.up_btn.setToolTip("Переместить вверх")
        self.up_btn.setStyleSheet(btn_style)
        self.up_btn.clicked.connect(lambda: self.movedUp.emit(self))
        layout.addWidget(self.up_btn)
        
        self.down_btn = QPushButton("▼")
        self.down_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.down_btn.setFixedSize(20, 20)
        self.down_btn.setToolTip("Переместить вниз")
        self.down_btn.setStyleSheet(btn_style)
        self.down_btn.clicked.connect(lambda: self.movedDown.emit(self))
        layout.addWidget(self.down_btn)
        
        self.edit_btn = QPushButton("✏️")
        self.edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.edit_btn.setFixedSize(20, 20)
        self.edit_btn.setToolTip("Редактировать свойства")
        self.edit_btn.setStyleSheet(btn_style)
        self.edit_btn.clicked.connect(lambda: self.selected.emit(self.field_data))
        layout.addWidget(self.edit_btn)
        
        self.delete_btn = QPushButton("🗑️")
        self.delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_btn.setFixedSize(20, 20)
        self.delete_btn.setToolTip("Удалить поле")
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #94a3b8;
                border: none;
                border-radius: 3px;
                font-size: 11px;
                padding: 0px;
                margin: 0px;
            }
            QPushButton:hover {
                background-color: #ef4444;
                color: white;
            }
            QPushButton:disabled {
                color: #475569;
            }
        """)
        self.delete_btn.clicked.connect(lambda: self.removed.emit(self))
        layout.addWidget(self.delete_btn)
    
    def _on_name_changed(self, text: str):
        if not self.isEnabled():
            return
        self.field_data['name_ru'] = text
        self.field_data['name_en'] = Translator.to_english(text)
        if hasattr(self.parent(), '_on_field_name_changed'):
            self.parent()._on_field_name_changed()
    
    def _update_indicators(self):
        if self.field_data.get('required'):
            self.required_label.setText("⚠️")
            self.required_label.setStyleSheet("font-size: 12px; color: #f59e0b;")
            self.required_label.setToolTip("Обязательное поле")
        else:
            self.required_label.setText("")
    
    def update_from_properties(self, properties: dict):
        if not self.isEnabled():
            return
        self.field_data.update(properties)
        self._update_indicators()
    
    def set_index(self, index: int):
        self.index = index
        self.num_label.setText(f"{index + 1}.")
    
    def set_buttons_state(self, is_first: bool, is_last: bool):
        if not self.isEnabled():
            return
        self.up_btn.setEnabled(not is_first)
        self.down_btn.setEnabled(not is_last)
    
    def set_selected(self, selected: bool):
        if not self.isEnabled():
            return
        self.setProperty("selected", selected)
        self.style().polish(self)
    
    def mousePressEvent(self, event):
        if self.isEnabled():
            self.selected.emit(self.field_data)
        super().mousePressEvent(event)
    
    # ========== КРИТИЧЕСКИ ВАЖНО: ИГНОРИРУЕМ ВСЕ DRAG СОБЫТИЯ ==========
    def dragEnterEvent(self, event):
        """Запрещаем вход - поле НИКОГДА не принимает данные"""
        event.ignore()
    
    def dragMoveEvent(self, event):
        """Запрещаем движение"""
        event.ignore()
    
    def dragLeaveEvent(self, event):
        """Игнорируем выход"""
        event.ignore()
    
    def dropEvent(self, event):
        """НИЧЕГО НЕ ПРИНИМАЕМ!"""
        event.ignore()