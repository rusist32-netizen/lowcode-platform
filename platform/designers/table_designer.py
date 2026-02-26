# -*- coding: utf-8 -*-

"""
Конструктор таблиц - ПОЛНАЯ БЛОКИРОВКА ПРИ ПЕРЕТАСКИВАНИИ
"""

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from platform.core.translator import Translator
from platform.core.field_types import FieldType
from platform.widgets.field_row import FieldRow
from platform.widgets.properties_panel import PropertiesPanel
from platform.designers.table_list_panel import TableListPanel
from platform.designers.field_tile_panel import FieldTilePanel


class TableDesignerWidget(QWidget):
    """Основной виджет конструктора таблиц"""
    
    def __init__(self, project_manager):
        super().__init__()
        
        self.project_manager = project_manager
        self.current_table = None
        self.current_field = None
        self.fields = []
        
        self.scroll_area = None
        self.drag_active = False
        self.add_field_btn = None
        self.fields_container = None
        self.properties_panel = None
        self.drop_hint = None
        self.fields_layout = None
        
        self._setup_ui()
        self._load_project_tables()
        
        # Подключаем сигналы от плиток с задержкой
        QTimer.singleShot(200, self._connect_all_tiles)
    
    def _connect_all_tiles(self):
        """Находит плитки в FieldTilePanel и подписывается на их состояние"""
        try:
            from platform.widgets.field_tile import FieldTile
            tiles = self.findChildren(FieldTile)
            print(f"🔍 Найдено плиток: {len(tiles)}")
            for tile in tiles:
                tile.dragStarted.connect(self.on_drag_started)
                tile.dragFinished.connect(self.on_drag_finished)
            print("✅ Сигналы плиток подключены")
        except Exception as e:
            print(f"❌ Ошибка подключения сигналов плиток: {e}")
    
    def on_drag_started(self):
        """Начало перетаскивания — блокируем редактирование всех существующих полей"""
        print("🔄 НАЧАЛО ПЕРЕТАСКИВАНИЯ - БЛОКИРУЕМ ПОЛЯ!")
        self.drag_active = True
        self._block_all_fields(True)
        
        # Визуальный отклик контейнера
        if hasattr(self, 'fields_container'):
            self.fields_container.setProperty("dragOver", True)
            self.fields_container.style().polish(self.fields_container)
    
    def on_drag_finished(self):
        """Конец перетаскивания — возвращаем поля в рабочее состояние"""
        print("✅ ЗАВЕРШЕНИЕ ПЕРЕТАСКИВАНИЯ - РАЗБЛОКИРУЕМ ПОЛЯ!")
        self.drag_active = False
        self._block_all_fields(False)
        
        if hasattr(self, 'fields_container'):
            self.fields_container.setProperty("dragOver", False)
            self.fields_container.style().polish(self.fields_container)
        
        if self.current_field:
            self.properties_panel.set_field(self.current_field)
    
    def _block_all_fields(self, block: bool):
        """Массовое управление доступностью полей"""
        try:
            if not hasattr(self, 'fields_layout'):
                return
                
            for i in range(self.fields_layout.count()):
                item = self.fields_layout.itemAt(i)
                if item and item.widget() and isinstance(item.widget(), FieldRow):
                    field_widget = item.widget()
                    # Блокируем ввод (QLineEdit станет серым) и кнопки
                    field_widget.setEnabled(not block)
                    # Строго запрещаем принимать Drop, чтобы данные не попали в QLineEdit
                    field_widget.setAcceptDrops(False)
                    if block:
                        field_widget.set_selected(False)
            
            # Блокируем сопутствующие панели
            if hasattr(self, 'add_field_btn'):
                self.add_field_btn.setEnabled(not block)
            if hasattr(self, 'table_list'):
                self.table_list.setEnabled(not block)
                
        except Exception as e:
            print(f"Ошибка при (раз)блокировке: {e}")
    
    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Левая панель
        self.table_list = TableListPanel()
        self.table_list.tableSelected.connect(self._on_table_selected)
        self.table_list.tableCreated.connect(self._on_table_created)
        layout.addWidget(self.table_list)
        
        # Центральная область
        center_panel = QWidget()
        center_layout = QVBoxLayout(center_panel)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(0)
        
        # Верхняя часть - информация о таблице
        table_info = QWidget()
        table_info.setStyleSheet("background-color: #1e293b; border-bottom: 1px solid #334155;")
        info_layout = QHBoxLayout(table_info)
        info_layout.setContentsMargins(15, 5, 15, 5)
        
        info_layout.addWidget(QLabel("Таблица:"))
        
        self.table_name_label = QLabel("—")
        self.table_name_label.setStyleSheet("color: #3b82f6; font-weight: bold; font-size: 13px;")
        info_layout.addWidget(self.table_name_label)
        
        self.table_name_edit = QLineEdit()
        self.table_name_edit.hide()
        self.table_name_edit.setFixedWidth(180)
        self.table_name_edit.setFixedHeight(24)
        self.table_name_edit.returnPressed.connect(self._save_table_name)
        info_layout.addWidget(self.table_name_edit)
        
        edit_name_btn = QPushButton("✏️")
        edit_name_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_name_btn.setFixedSize(24, 24)
        edit_name_btn.setToolTip("Изменить название")
        edit_name_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                border-radius: 3px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        edit_name_btn.clicked.connect(self._edit_table_name)
        info_layout.addWidget(edit_name_btn)
        
        info_layout.addStretch()
        center_layout.addWidget(table_info)
        
        # Контейнер для полей с прокруткой
        fields_container = QWidget()
        fields_container.setStyleSheet("background-color: #0f172a;")
        container_layout = QVBoxLayout(fields_container)
        container_layout.setContentsMargins(15, 10, 15, 10)
        container_layout.setSpacing(8)
        
        # Заголовок с кнопкой добавления
        header_layout = QHBoxLayout()
        header_layout.setSpacing(5)
        
        header = QLabel("📋 ПОЛЯ ТАБЛИЦЫ")
        header.setStyleSheet("color: #3b82f6; font-size: 14px; font-weight: bold;")
        header_layout.addWidget(header)
        
        header_layout.addStretch()
        
        self.add_field_btn = QPushButton("➕ Добавить поле")
        self.add_field_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_field_btn.setFixedSize(100, 24)
        self.add_field_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: white;
                border: none;
                border-radius: 3px;
                font-weight: 500;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        self.add_field_btn.clicked.connect(self._add_field_manually)
        header_layout.addWidget(self.add_field_btn)
        
        container_layout.addLayout(header_layout)
        
        # Область для полей с прокруткой
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: 1px solid #334155;
                border-radius: 4px;
                background-color: #1e293b;
            }
            QScrollBar:vertical {
                background-color: #1e293b;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background-color: #475569;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #3b82f6;
            }
        """)
        
        # КОНТЕЙНЕР ДЛЯ ПОЛЕЙ - ТОЛЬКО ОН ПРИНИМАЕТ DROP
        self.fields_container = QWidget()
        self.fields_container.setAcceptDrops(True)
        self.fields_container.setStyleSheet("""
            QWidget {
                background-color: transparent;
            }
            QWidget[dragOver="true"] {
                background-color: rgba(59, 130, 246, 0.1);
                border: 2px dashed #3b82f6;
            }
        """)
        
        self.fields_layout = QVBoxLayout(self.fields_container)
        self.fields_layout.setContentsMargins(4, 4, 4, 4)
        self.fields_layout.setSpacing(2)
        self.fields_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Подсказка
        self.drop_hint = QLabel("Перетащите типы полей сюда")
        self.drop_hint.setStyleSheet("color: #64748b; font-size: 12px; padding: 20px;")
        self.drop_hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.fields_layout.addWidget(self.drop_hint)
        
        self.scroll_area.setWidget(self.fields_container)
        container_layout.addWidget(self.scroll_area, 1)
        
        center_layout.addWidget(fields_container, 1)
        
        # Нижняя часть - панель свойств
        self.properties_panel = PropertiesPanel()
        self.properties_panel.setMaximumHeight(220)
        center_layout.addWidget(self.properties_panel)
        
        layout.addWidget(center_panel, 1)
        
        # Правая панель
        self.field_tiles = FieldTilePanel()
        layout.addWidget(self.field_tiles)
        
        # Подключаем события для контейнера
        self.fields_container.dragEnterEvent = self.container_dragEnterEvent
        self.fields_container.dragMoveEvent = self.container_dragMoveEvent
        self.fields_container.dragLeaveEvent = self.container_dragLeaveEvent
        self.fields_container.dropEvent = self.container_dropEvent
    
    def _load_project_tables(self):
        if not self.project_manager.current_project:
            return
        
        for table_data in self.project_manager.current_project.tables:
            self.table_list.add_table(table_data)
        
        self.properties_panel.set_tables(self.table_list.get_tables())
    
    def _on_table_selected(self, table_data: dict):
        self.current_table = table_data
        self.fields = table_data.get('fields', [])
        self.table_name_label.setText(table_data['name_ru'])
        self.table_name_label.show()
        self.table_name_edit.hide()
        self.properties_panel.set_current_table(table_data['id'])
        self._refresh_fields_display()
        self.current_field = None
        self.properties_panel.set_field(None)
    
    def _on_table_created(self):
        self._save_table_data()
        self.properties_panel.set_tables(self.table_list.get_tables())
    
    def _edit_table_name(self):
        if not self.current_table:
            return
        self.table_name_label.hide()
        self.table_name_edit.setText(self.current_table['name_ru'])
        self.table_name_edit.show()
        self.table_name_edit.setFocus()
        self.table_name_edit.selectAll()
    
    def _save_table_name(self):
        if not self.current_table:
            return
        new_name = self.table_name_edit.text().strip()
        if new_name:
            self.current_table['name_ru'] = new_name
            self.current_table['name_en'] = Translator.to_english(new_name)
            self.table_list.update_table(self.current_table)
            self.table_name_label.setText(new_name)
        self.table_name_label.show()
        self.table_name_edit.hide()
        self._save_table_data()
    
    def _refresh_fields_display(self):
        for i in reversed(range(self.fields_layout.count())):
            item = self.fields_layout.itemAt(i)
            if item and item.widget() and item.widget() != self.drop_hint:
                item.widget().deleteLater()
        
        if not self.fields:
            self.drop_hint.show()
            return
        
        self.drop_hint.hide()
        
        for i, field_data in enumerate(self.fields):
            row = FieldRow(field_data, i, self.table_list.get_tables(), self)
            row.movedUp.connect(self._move_field_up)
            row.movedDown.connect(self._move_field_down)
            row.removed.connect(self._remove_field)
            row.selected.connect(self._on_field_selected)
            row.name_edit.textChanged.connect(self._on_field_name_changed)
            
            # Запрещаем принимать drop
            row.setAcceptDrops(False)
            
            self.fields_layout.addWidget(row)
        
        self._update_field_buttons_state()
    
    def _move_field_up(self, row: FieldRow):
        if self.drag_active:
            return
        current_index = self.fields_layout.indexOf(row)
        if current_index > 0:
            self.fields_layout.removeWidget(row)
            self.fields_layout.insertWidget(current_index - 1, row)
            row_data = self.fields.pop(current_index)
            self.fields.insert(current_index - 1, row_data)
            self._renumber_fields()
            self._update_field_buttons_state()
            self._save_table_data()
    
    def _move_field_down(self, row: FieldRow):
        if self.drag_active:
            return
        current_index = self.fields_layout.indexOf(row)
        if current_index < len(self.fields) - 1:
            self.fields_layout.removeWidget(row)
            self.fields_layout.insertWidget(current_index + 1, row)
            row_data = self.fields.pop(current_index)
            self.fields.insert(current_index + 1, row_data)
            self._renumber_fields()
            self._update_field_buttons_state()
            self._save_table_data()
    
    def _renumber_fields(self):
        for i in range(self.fields_layout.count()):
            item = self.fields_layout.itemAt(i)
            if item and item.widget() and isinstance(item.widget(), FieldRow):
                item.widget().set_index(i)
    
    def _update_field_buttons_state(self):
        if self.drag_active:
            return
        fields = []
        for i in range(self.fields_layout.count()):
            item = self.fields_layout.itemAt(i)
            if item and item.widget() and isinstance(item.widget(), FieldRow):
                fields.append(item.widget())
        for i, widget in enumerate(fields):
            widget.set_buttons_state(i == 0, i == len(fields) - 1)
    
    def _on_field_selected(self, field_data: dict):
        if self.drag_active:
            return
        self.current_field = field_data
        for i in range(self.fields_layout.count()):
            item = self.fields_layout.itemAt(i)
            if item and item.widget() and isinstance(item.widget(), FieldRow):
                item.widget().set_selected(item.widget().field_data['id'] == field_data['id'])
        self.properties_panel.set_field(field_data)
        print(f"✅ Поле выбрано: {field_data.get('name_ru', 'без имени')}")
    
    def _on_field_name_changed(self):
        if self.drag_active:
            return
        self._save_table_data()
    
    def _remove_field(self, row: FieldRow):
        if self.drag_active:
            return
        if row.field_data in self.fields:
            index = self.fields.index(row.field_data)
            self.fields.pop(index)
            row.deleteLater()
            self._renumber_fields()
            self._update_field_buttons_state()
            if self.current_field and self.current_field['id'] == row.field_data['id']:
                self.current_field = None
                self.properties_panel.set_field(None)
            self._save_table_data()
    
    def _on_properties_changed(self, properties: dict):
        if self.drag_active or not self.current_field:
            return
        self.current_field.update(properties)
        for i in range(self.fields_layout.count()):
            item = self.fields_layout.itemAt(i)
            if item and item.widget() and isinstance(item.widget(), FieldRow):
                if item.widget().field_data['id'] == self.current_field['id']:
                    item.widget().update_from_properties(properties)
                    break
        self._save_table_data()
    
    def _create_field_from_type(self, type_id: str) -> dict:
        from platform.core.field_types import FieldType
        icon, full_type_name, desc, tid = FieldType.get_type_by_id(type_id)
        field_id = f"field_{len(self.fields)}_{Translator.to_english(full_type_name)}_{len(self.fields)}"
        return {
            'id': field_id,
            'name_ru': '',
            'name_en': '',
            'type': full_type_name,
            'type_id': type_id,
            'required': False,
            'unique': False,
            'default': None,
            'format': {}
        }
    
    def _add_field_manually(self):
        if self.drag_active or not self.current_table:
            return
        types = [f"{icon} {name}" for icon, name, _, _ in FieldType.TYPES]
        type_name, ok = QInputDialog.getItem(self, "Выберите тип поля", "Тип:", types, 0, False)
        if ok and type_name:
            clean_name = type_name.split(' ', 1)[-1] if ' ' in type_name else type_name
            type_id = FieldType.get_type_id(clean_name)
            field_data = self._create_field_from_type(type_id)
            self.fields.append(field_data)
            self._refresh_fields_display()
            self._save_table_data()
            self.current_field = field_data
            self.properties_panel.set_field(field_data)
            QTimer.singleShot(100, self._scroll_to_bottom)
    
    def _scroll_to_bottom(self):
        if self.scroll_area:
            self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())
    
    # ==================== DRAG & DROP МЕТОДЫ ДЛЯ КОНТЕЙНЕРА ====================
    
    def container_dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            event.ignore()
    
    def container_dragMoveEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()
    
    def container_dragLeaveEvent(self, event):
        if hasattr(self, 'fields_container'):
            self.fields_container.setProperty("dragOver", False)
            self.fields_container.style().polish(self.fields_container)
    
    def container_dropEvent(self, event):
        try:
            # Разблокируем все сразу после сброса
            self.on_drag_finished()
            
            if not self.current_table:
                QMessageBox.warning(self, "Внимание", "Сначала выберите таблицу")
                return
            
            text = event.mimeData().text()
            if text:
                type_id = text.split(':')[0]
                field_data = self._create_field_from_type(type_id)
                self.fields.append(field_data)
                self._refresh_fields_display()
                self._save_table_data()
                
                # Авто-прокрутка вниз к новому полю
                QTimer.singleShot(100, self._scroll_to_bottom)
                event.acceptProposedAction()
        except Exception as e:
            print(f"Ошибка при сбросе поля: {e}")
    
    def _save_table_data(self):
        if not self.current_table or self.drag_active:
            return
        self.current_table['fields'] = self.fields
        found = False
        for i, table in enumerate(self.project_manager.current_project.tables):
            if table['id'] == self.current_table['id']:
                self.project_manager.current_project.tables[i] = self.current_table
                found = True
                break
        if not found:
            self.project_manager.current_project.tables.append(self.current_table)
        self.project_manager.save_project()
    
    def can_close(self) -> bool:
        return True