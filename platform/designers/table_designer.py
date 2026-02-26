#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Конструктор таблиц (основной файл)
"""

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from ..widgets.property_panel import PropertyPanel
from ..widgets.table_viewer import TableViewer
from ..dialogs.formula_dialog import FormulaDialog
from .field_tile_panel import FieldTilePanel
from .table_list_panel import TableListPanel


class TableDesigner(QWidget):
    """
    Главный класс конструктора таблиц
    """

    tableChanged = pyqtSignal()  # сигнал об изменении таблицы
    fieldSelected = pyqtSignal(object)  # сигнал о выборе поля

    def __init__(self, project_manager, parent=None):
        super().__init__(parent)
        self.project_manager = project_manager
        self.current_table = None
        self.current_field = None
        self.fields = []  # список полей текущей таблицы

        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        """Создание интерфейса конструктора"""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(1)

        # ===== ЛЕВАЯ ПАНЕЛЬ =====
        self.left_panel = QWidget()
        self.left_panel.setFixedWidth(250)
        self.left_panel.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                border-right: 1px solid #3c3c3c;
            }
        """)

        left_layout = QVBoxLayout(self.left_panel)
        left_layout.setContentsMargins(8, 8, 8, 8)
        left_layout.setSpacing(8)

        # Заголовок
        title = QLabel("КОНСТРУКТОР ТАБЛИЦ")
        title.setStyleSheet("""
            QLabel {
                color: #4ec9b0;
                font-weight: bold;
                font-size: 12px;
                padding: 4px;
                border-bottom: 1px solid #3c3c3c;
            }
        """)
        left_layout.addWidget(title)

        # Список таблиц
        self.table_list = TableListPanel(self.project_manager)
        self.table_list.tableSelected.connect(self.on_table_selected)
        self.table_list.tableCreated.connect(self.on_table_created)
        self.table_list.tableDeleted.connect(self.on_table_deleted)
        left_layout.addWidget(self.table_list, 1)

        main_layout.addWidget(self.left_panel)

        # ===== ЦЕНТРАЛЬНАЯ ОБЛАСТЬ =====
        # Вертикальный сплиттер для конструктора и просмотра
        self.vsplitter = QSplitter(Qt.Orientation.Vertical)

        # Верхняя часть - конструктор полей (2/3)
        self.designer_widget = self.create_designer_area()
        self.vsplitter.addWidget(self.designer_widget)

        # Нижняя часть - просмотр таблицы (1/3)
        self.table_viewer = TableViewer()
        self.vsplitter.addWidget(self.table_viewer)

        # Устанавливаем соотношение 2:1
        self.vsplitter.setSizes([666, 333])

        main_layout.addWidget(self.vsplitter, 1)

        # ===== ПРАВАЯ ПАНЕЛЬ =====
        self.right_panel = QWidget()
        self.right_panel.setFixedWidth(300)
        self.right_panel.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                border-left: 1px solid #3c3c3c;
            }
        """)

        right_layout = QVBoxLayout(self.right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        # Панель свойств
        self.properties_panel = PropertyPanel()
        self.properties_panel.propertyChanged.connect(self.on_property_changed)

        right_layout.addWidget(self.properties_panel)

        main_layout.addWidget(self.right_panel)

    def create_designer_area(self):
        """Создаёт область конструктора полей"""
        widget = QWidget()
        widget.setStyleSheet("""
            QWidget {
                background-color: #252526;
            }
        """)

        layout = QVBoxLayout(widget)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # Панель с плитками полей
        self.tile_panel = FieldTilePanel()
        self.tile_panel.fieldTileClicked.connect(self.on_field_tile_clicked)
        layout.addWidget(self.tile_panel)

        # Область для размещения полей таблицы
        self.fields_area = QScrollArea()
        self.fields_area.setWidgetResizable(True)
        self.fields_area.setFrameShape(QFrame.Shape.NoFrame)
        self.fields_area.setStyleSheet("""
            QScrollArea {
                background-color: #1e1e1e;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
            }
        """)

        self.fields_container = QWidget()
        self.fields_container.setStyleSheet("background-color: #1e1e1e;")

        self.fields_layout = QVBoxLayout(self.fields_container)
        self.fields_layout.setContentsMargins(8, 8, 8, 8)
        self.fields_layout.setSpacing(4)
        self.fields_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.fields_area.setWidget(self.fields_container)
        layout.addWidget(self.fields_area, 1)

        # Кнопки управления
        btn_layout = QHBoxLayout()

        self.save_btn = QPushButton("💾 Сохранить таблицу")
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #0e639c;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1177bb;
            }
        """)
        self.save_btn.clicked.connect(self.save_table)

        self.preview_btn = QPushButton("👁️ Предпросмотр")
        self.preview_btn.setStyleSheet("""
            QPushButton {
                background-color: #4c4c4c;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #5c5c5c;
            }
        """)
        self.preview_btn.clicked.connect(self.toggle_preview)

        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.preview_btn)

        layout.addLayout(btn_layout)

        return widget

    def connect_signals(self):
        """Подключает сигналы"""
        # Здесь можно добавить дополнительные соединения
        pass

    # ========== МЕТОДЫ ДЛЯ РАБОТЫ С ТАБЛИЦАМИ ==========

    def on_table_selected(self, table_data):
        """Выбрана таблица в списке"""
        self.current_table = table_data
        self.load_table_fields(table_data)

        # Загружаем данные таблицы для просмотра
        data = self.project_manager.get_table_data(table_data['id'])
        self.table_viewer.set_table(table_data, data)

        # Показываем свойства таблицы
        self.properties_panel.set_table(table_data)

        self.tableChanged.emit()

    def on_table_created(self, table_data):
        """Создана новая таблица"""
        self.current_table = table_data
        self.clear_fields()
        self.properties_panel.set_table(table_data)

    def on_table_deleted(self, table_id):
        """Удалена таблица"""
        if self.current_table and self.current_table['id'] == table_id:
            self.current_table = None
            self.clear_fields()
            self.properties_panel.clear()

    def load_table_fields(self, table_data):
        """Загружает поля таблицы"""
        self.clear_fields()
        fields = table_data.get('fields', [])

        for field in fields:
            self.add_field_widget(field)

    def clear_fields(self):
        """Очищает область полей"""
        while self.fields_layout.count():
            item = self.fields_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.fields = []

    def add_field_widget(self, field_data):
        """Добавляет виджет поля в область"""
        from .field_widget import FieldWidget

        widget = FieldWidget(field_data)
        widget.fieldClicked.connect(self.on_field_clicked)
        widget.fieldMoved.connect(self.on_field_moved)
        widget.fieldDeleted.connect(self.on_field_deleted)

        self.fields_layout.addWidget(widget)
        self.fields.append({
            'widget': widget,
            'data': field_data
        })

    # ========== МЕТОДЫ ДЛЯ РАБОТЫ С ПОЛЯМИ ==========

    def on_field_tile_clicked(self, field_type):
        """Клик по плитке поля - создание нового поля"""
        if not self.current_table:
            QMessageBox.warning(self, "Внимание", "Сначала выберите или создайте таблицу")
            return

        # Создаём новое поле
        field_data = self.create_new_field(field_type)
        self.add_field_widget(field_data)

        # Выделяем новое поле
        self.on_field_clicked(field_data)

    def create_new_field(self, field_type):
        """Создаёт новое поле заданного типа"""
        from ..core.field_types import FieldType

        # Определяем тип
        if isinstance(field_type, str):
            try:
                type_enum = FieldType[field_type]
            except:
                type_enum = FieldType.TEXT
        else:
            type_enum = field_type

        # Базовая структура поля
        field = {
            'id': f"field_{len(self.fields) + 1}",
            'display_name': f"Поле {len(self.fields) + 1}",
            'type': type_enum,
            'required': False,
            'unique': False,
            'default': '',
            'description': '',
            'width': 150,
            'visible': True,
            'readonly': False
        }

        # Добавляем специфические свойства в зависимости от типа
        type_name = type_enum.value if hasattr(type_enum, 'value') else str(type_enum)

        if type_name in ['TEXT', 'Текст']:
            field['text_format'] = 'Как написано'
            field['max_length'] = 255
            field['input_mask'] = 'Без маски'

        elif type_name in ['TEXT_MULTILINE', 'Многострочный текст']:
            field['multiline_format'] = 'Обычный текст'
            field['height'] = 5
            field['word_wrap'] = True

        elif type_name in ['INTEGER', 'Целое число']:
            field['min_value'] = 0
            field['max_value'] = 100
            field['use_thousands'] = False

        elif type_name in ['FLOAT', 'Дробное число']:
            field['decimals'] = 2
            field['min_value'] = 0
            field['max_value'] = 100
            field['use_thousands'] = False

        elif type_name in ['MONEY', 'Деньги']:
            field['currency'] = '₽ (Рубль)'
            field['decimals'] = 2
            field['min_value'] = 0
            field['max_value'] = 999999

        elif type_name in ['PERCENT', 'Процент']:
            field['decimals'] = 1
            field['show_percent_sign'] = True
            field['min_value'] = 0
            field['max_value'] = 100

        elif type_name in ['DATE', 'Дата']:
            field['date_format'] = 'ДД.ММ.ГГГГ'
            field['time_format'] = 'Без времени'
            field['auto_current'] = False

        elif type_name in ['LIST', 'Список']:
            field['options'] = ['Вариант 1', 'Вариант 2', 'Вариант 3']
            field['list_type'] = 'Выпадающий список'
            field['sort_type'] = 'Как введено'

        elif type_name in ['REFERENCE', 'Ссылка']:
            field['reference_table'] = ''
            field['reference_display'] = ''
            field['relation_type'] = 'Одна запись'

        elif type_name in ['CALCULATED', 'Вычисляемое']:
            field['formula'] = ''
            field['result_type'] = 'Текст'

        return field

    def on_field_clicked(self, field_data):
        """Клик по полю - выделение и показ свойств"""
        self.current_field = field_data

        # Снимаем выделение со всех полей
        for field in self.fields:
            field['widget'].set_selected(False)

        # Выделяем текущее поле
        for field in self.fields:
            if field['data']['id'] == field_data['id']:
                field['widget'].set_selected(True)
                break

        # Показываем свойства поля
        self.properties_panel.set_field(field_data)
        self.table_viewer.on_field_selected(field_data)
        self.fieldSelected.emit(field_data)

    def on_field_moved(self, from_index, to_index):
        """Перемещение поля"""
        if 0 <= from_index < len(self.fields) and 0 <= to_index < len(self.fields):
            # Перемещаем в списке
            field = self.fields.pop(from_index)
            self.fields.insert(to_index, field)

            # Перемещаем виджет
            widget = field['widget']
            self.fields_layout.removeWidget(widget)
            self.fields_layout.insertWidget(to_index, widget)

            # Обновляем порядок
            self.update_field_order()

    def on_field_deleted(self, field_data):
        """Удаление поля"""
        reply = QMessageBox.question(
            self, "Подтверждение",
            f"Удалить поле '{field_data.get('display_name', '')}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Находим и удаляем
            for i, field in enumerate(self.fields):
                if field['data']['id'] == field_data['id']:
                    field['widget'].deleteLater()
                    self.fields.pop(i)
                    break

            if self.current_field and self.current_field['id'] == field_data['id']:
                self.current_field = None
                self.properties_panel.clear()

            self.update_field_order()

    def on_property_changed(self, prop_name, value):
        """Изменение свойства в панели"""
        if self.current_field:
            self.current_field[prop_name] = value

            # Обновляем отображение поля
            for field in self.fields:
                if field['data']['id'] == self.current_field['id']:
                    field['widget'].update_display(self.current_field)
                    break

    def update_field_order(self):
        """Обновляет порядок полей"""
        for i, field in enumerate(self.fields):
            field['data']['order'] = i

    # ========== МЕТОДЫ СОХРАНЕНИЯ ==========

    def save_table(self):
        """Сохраняет текущую таблицу"""
        if not self.current_table:
            QMessageBox.warning(self, "Внимание", "Нет таблицы для сохранения")
            return

        # Собираем поля
        fields_data = [field['data'] for field in self.fields]

        # Обновляем таблицу в project_manager
        self.current_table['fields'] = fields_data
        self.project_manager.update_table(self.current_table)

        # Обновляем список таблиц
        self.table_list.refresh()

        QMessageBox.information(self, "Успех", "Таблица сохранена")

    def toggle_preview(self):
        """Переключает режим предпросмотра"""
        # TODO: реализовать предпросмотр формы
        pass