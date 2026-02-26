#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Умная таблица свойств с поддержкой разных типов редакторов
"""

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import re

class PropertyItem:
    """Класс для хранения информации о свойстве"""
    
    def __init__(self, name, display_name, value=None, property_type="text", 
                 options=None, category="Основные", description="", 
                 enabled=True, visible=True):
        self.name = name                # системное имя
        self.display_name = display_name # отображаемое имя
        self.value = value               # текущее значение
        self.property_type = property_type  # text, number, bool, color, font, file, image, list, password
        self.options = options or []      # для выпадающих списков
        self.category = category          # категория для группировки
        self.description = description    # подсказка
        self.enabled = enabled
        self.visible = visible
        self.changed = False

class PropertyGrid(QTableWidget):
    """
    Таблица свойств с автоматическим созданием редакторов
    """
    
    propertyChanged = pyqtSignal(str, object)  # имя свойства, новое значение
    editingFinished = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.properties = []  # список PropertyItem
        self.editors = {}     # словарь редакторов по имени свойства
        self.category_rows = {}  # строки категорий
        self.setup_ui()
        
    def setup_ui(self):
        """Настройка внешнего вида таблицы"""
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(["Свойство", "Значение"])
        
        # Настройка внешнего вида
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setStretchLastSection(True)
        self.setAlternatingRowColors(True)
        
        # Стилизация
        self.setStyleSheet("""
            QTableWidget {
                background-color: #1e1e1e;
                color: #e0e0e0;
                gridline-color: #333333;
                outline: none;
            }
            QTableWidget::item {
                padding: 4px;
                border-bottom: 1px solid #333333;
            }
            QTableWidget::item:selected {
                background-color: #264f78;
            }
            QHeaderView::section {
                background-color: #2d2d2d;
                color: #e0e0e0;
                padding: 4px;
                border: 1px solid #3c3c3c;
                font-weight: bold;
            }
            QTableWidget QLineEdit, QTableWidget QComboBox, QTableWidget QSpinBox {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #3c3c3c;
                border-radius: 2px;
                padding: 2px;
            }
            QTableWidget QCheckBox {
                margin-left: 4px;
            }
            QTableWidget QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
        """)
        
        # Подключение сигналов
        self.itemSelectionChanged.connect(self.on_selection_changed)
        self.cellDoubleClicked.connect(self.on_cell_double_clicked)
        
    def set_properties(self, properties):
        """Устанавливает список свойств для отображения"""
        self.clear()
        self.properties = properties
        self.editors.clear()
        self.category_rows.clear()
        
        # Группировка по категориям
        categories = {}
        for prop in properties:
            if not prop.visible:
                continue
            if prop.category not in categories:
                categories[prop.category] = []
            categories[prop.category].append(prop)
        
        # Заполнение таблицы
        row = 0
        for category, props in categories.items():
            # Добавляем строку-заголовок категории
            self.insertRow(row)
            self.category_rows[category] = row
            self.setSpan(row, 0, 1, 2)
            cat_item = QTableWidgetItem(f" {category}")
            cat_item.setBackground(QColor("#2d2d2d"))
            cat_item.setForeground(QColor("#4ec9b0"))
            cat_item.setFlags(Qt.ItemFlag.ItemIsEnabled)
            font = QFont()
            font.setBold(True)
            cat_item.setFont(font)
            self.setItem(row, 0, cat_item)
            row += 1
            
            # Добавляем свойства категории
            for prop in props:
                self.insertRow(row)
                
                # Название свойства
                name_item = QTableWidgetItem(f"  {prop.display_name}")
                name_item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                name_item.setToolTip(prop.description)
                name_item.setForeground(QColor("#9cdcfe"))
                self.setItem(row, 0, name_item)
                
                # Редактор значения
                editor = self.create_editor(prop, row)
                if editor:
                    self.editors[prop.name] = editor
                    self.setCellWidget(row, 1, editor)
                
                row += 1
        
        self.setRowCount(row)
        self.resizeColumnToContents(0)
        
    def create_editor(self, prop, row):
        """Создаёт редактор для свойства в зависимости от типа"""
        editor = None
        
        if prop.property_type == "text":
            editor = QLineEdit()
            editor.setText(str(prop.value) if prop.value is not None else "")
            editor.textChanged.connect(lambda text, p=prop: self.on_text_changed(p, text))
            editor.editingFinished.connect(self.editingFinished.emit)
            
        elif prop.property_type == "number":
            editor = QSpinBox()
            if isinstance(prop.options, dict):
                if "min" in prop.options:
                    editor.setMinimum(prop.options["min"])
                if "max" in prop.options:
                    editor.setMaximum(prop.options["max"])
            editor.setValue(int(prop.value) if prop.value is not None else 0)
            editor.valueChanged.connect(lambda val, p=prop: self.on_value_changed(p, val))
            
        elif prop.property_type == "float":
            editor = QDoubleSpinBox()
            if isinstance(prop.options, dict):
                if "min" in prop.options:
                    editor.setMinimum(prop.options["min"])
                if "max" in prop.options:
                    editor.setMaximum(prop.options["max"])
                if "decimals" in prop.options:
                    editor.setDecimals(prop.options["decimals"])
            editor.setValue(float(prop.value) if prop.value is not None else 0.0)
            editor.valueChanged.connect(lambda val, p=prop: self.on_value_changed(p, val))
            
        elif prop.property_type == "bool":
            editor = QCheckBox()
            editor.setChecked(bool(prop.value))
            editor.stateChanged.connect(lambda state, p=prop: self.on_bool_changed(p, state))
            
        elif prop.property_type == "combobox":
            editor = QComboBox()
            if prop.options:
                editor.addItems([str(opt) for opt in prop.options])
            if prop.value is not None:
                index = editor.findText(str(prop.value))
                if index >= 0:
                    editor.setCurrentIndex(index)
            editor.currentTextChanged.connect(lambda text, p=prop: self.on_combobox_changed(p, text))
            
        elif prop.property_type == "color":
            editor = QPushButton()
            editor.setText(prop.value if prop.value else "#000000")
            editor.setStyleSheet(f"background-color: {prop.value if prop.value else '#000000'};")
            editor.clicked.connect(lambda checked, p=prop: self.on_color_picker(p))
            
        elif prop.property_type == "font":
            editor = QPushButton()
            editor.setText(prop.value if prop.value else "System")
            editor.clicked.connect(lambda checked, p=prop: self.on_font_picker(p))
            
        elif prop.property_type == "file":
            widget = QWidget()
            layout = QHBoxLayout(widget)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(2)
            
            line_edit = QLineEdit()
            line_edit.setText(prop.value if prop.value else "")
            line_edit.setReadOnly(True)
            
            browse_btn = QPushButton("...")
            browse_btn.setMaximumWidth(30)
            browse_btn.clicked.connect(lambda checked, p=prop, le=line_edit: self.on_file_picker(p, le))
            
            clear_btn = QPushButton("✕")
            clear_btn.setMaximumWidth(30)
            clear_btn.clicked.connect(lambda checked, p=prop, le=line_edit: self.on_file_clear(p, le))
            
            layout.addWidget(line_edit)
            layout.addWidget(browse_btn)
            layout.addWidget(clear_btn)
            editor = widget
            
        elif prop.property_type == "password":
            editor = QLineEdit()
            editor.setText(prop.value if prop.value else "")
            editor.setEchoMode(QLineEdit.EchoMode.Password)
            editor.textChanged.connect(lambda text, p=prop: self.on_text_changed(p, text))
            
        if editor:
            editor.setEnabled(prop.enabled)
            
        return editor
    
    def on_text_changed(self, prop, text):
        """Обработка изменения текста"""
        old_value = prop.value
        prop.value = text
        prop.changed = (old_value != text)
        self.propertyChanged.emit(prop.name, text)
        
    def on_value_changed(self, prop, value):
        """Обработка изменения числового значения"""
        old_value = prop.value
        prop.value = value
        prop.changed = (old_value != value)
        self.propertyChanged.emit(prop.name, value)
        
    def on_bool_changed(self, prop, state):
        """Обработка изменения булева значения"""
        value = (state == Qt.CheckState.Checked.value)
        old_value = prop.value
        prop.value = value
        prop.changed = (old_value != value)
        self.propertyChanged.emit(prop.name, value)
        
    def on_combobox_changed(self, prop, text):
        """Обработка изменения выпадающего списка"""
        old_value = prop.value
        prop.value = text
        prop.changed = (old_value != text)
        self.propertyChanged.emit(prop.name, text)
        
    def on_color_picker(self, prop):
        """Выбор цвета"""
        color = QColorDialog.getColor(QColor(prop.value) if prop.value else QColor())
        if color.isValid():
            hex_color = color.name()
            prop.value = hex_color
            prop.changed = True
            
            # Обновляем кнопку
            btn = self.sender()
            btn.setText(hex_color)
            btn.setStyleSheet(f"background-color: {hex_color};")
            
            self.propertyChanged.emit(prop.name, hex_color)
            
    def on_font_picker(self, prop):
        """Выбор шрифта"""
        current_font = QFont(prop.value) if prop.value else QFont()
        font, ok = QFontDialog.getFont(current_font)
        if ok:
            font_name = font.family()
            prop.value = font_name
            prop.changed = True
            
            # Обновляем кнопку
            btn = self.sender()
            btn.setText(font_name)
            
            self.propertyChanged.emit(prop.name, font_name)
            
    def on_file_picker(self, prop, line_edit):
        """Выбор файла"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите файл", "", 
            prop.options.get("filter", "Все файлы (*.*)") if isinstance(prop.options, dict) else "Все файлы (*.*)"
        )
        if file_path:
            line_edit.setText(file_path)
            prop.value = file_path
            prop.changed = True
            self.propertyChanged.emit(prop.name, file_path)
            
    def on_file_clear(self, prop, line_edit):
        """Очистка выбора файла"""
        line_edit.clear()
        prop.value = ""
        prop.changed = True
        self.propertyChanged.emit(prop.name, "")
        
    def on_selection_changed(self):
        """Обработка изменения выделения"""
        current_row = self.currentRow()
        if current_row >= 0:
            # Прокручиваем к выделенной строке
            self.scrollToItem(self.currentItem())
            
    def on_cell_double_clicked(self, row, col):
        """Обработка двойного клика"""
        if col == 1:  # Кликнули по колонке со значением
            # Фокусируемся на редакторе
            widget = self.cellWidget(row, col)
            if widget:
                widget.setFocus()
                
    def get_property_value(self, name):
        """Возвращает значение свойства по имени"""
        for prop in self.properties:
            if prop.name == name:
                return prop.value
        return None
        
    def set_property_value(self, name, value):
        """Устанавливает значение свойства"""
        for prop in self.properties:
            if prop.name == name:
                prop.value = value
                # Обновляем редактор
                editor = self.editors.get(name)
                if editor:
                    if isinstance(editor, QLineEdit):
                        editor.setText(str(value))
                    elif isinstance(editor, (QSpinBox, QDoubleSpinBox)):
                        editor.setValue(value)
                    elif isinstance(editor, QCheckBox):
                        editor.setChecked(bool(value))
                    elif isinstance(editor, QComboBox):
                        index = editor.findText(str(value))
                        if index >= 0:
                            editor.setCurrentIndex(index)
                break
                
    def get_changed_properties(self):
        """Возвращает список изменённых свойств"""
        return [prop for prop in self.properties if prop.changed]
        
    def reset_changed_flags(self):
        """Сбрасывает флаги изменений"""
        for prop in self.properties:
            prop.changed = False