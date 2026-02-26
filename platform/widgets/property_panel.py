#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Панель свойств для конструктора таблиц
"""

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class PropertySection(QWidget):
    """Базовый класс для секции свойств"""

    changed = pyqtSignal(str, object)

    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.title = title
        self.setup_ui()

    def setup_ui(self):
        """Создание заголовка секции"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        # Заголовок секции
        title_label = QLabel(self.title)
        title_label.setStyleSheet("""
            QLabel {
                color: #4ec9b0;
                font-weight: bold;
                font-size: 11px;
                padding: 4px 0px;
                border-bottom: 1px solid #3c3c3c;
            }
        """)
        layout.addWidget(title_label)

        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(8, 4, 8, 8)
        self.content_layout.setSpacing(6)
        layout.addWidget(self.content)

    def add_checkbox(self, name, label, value=False):
        """Добавляет чекбокс"""
        cb = QCheckBox(label)
        cb.setChecked(value)
        cb.setStyleSheet("""
            QCheckBox {
                color: #e0e0e0;
                font-size: 12px;
                spacing: 6px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 1px solid #4c4c4c;
                background-color: #2d2d2d;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                background-color: #0e639c;
                border: 1px solid #0e639c;
                image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='white' width='16px' height='16px'><path d='M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z'/></svg>");
            }
        """)
        cb.stateChanged.connect(lambda state, n=name: self.changed.emit(n, state == Qt.CheckState.Checked.value))
        self.content_layout.addWidget(cb)
        return cb

    def add_lineedit(self, name, label, value="", placeholder=""):
        """Добавляет поле ввода"""
        w = QWidget()
        layout = QHBoxLayout(w)
        layout.setContentsMargins(0, 0, 0, 0)

        lbl = QLabel(label)
        lbl.setStyleSheet("color: #9cdcfe; font-size: 12px; min-width: 100px;")

        edit = QLineEdit(value)
        edit.setPlaceholderText(placeholder)
        edit.setStyleSheet("""
            QLineEdit {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #4c4c4c;
                border-radius: 3px;
                padding: 4px 6px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 1px solid #0e639c;
            }
        """)
        edit.textChanged.connect(lambda text, n=name: self.changed.emit(n, text))

        layout.addWidget(lbl)
        layout.addWidget(edit)
        self.content_layout.addWidget(w)
        return edit

    def add_combobox(self, name, label, value="", items=None):
        """Добавляет выпадающий список"""
        if items is None:
            items = []

        w = QWidget()
        layout = QHBoxLayout(w)
        layout.setContentsMargins(0, 0, 0, 0)

        lbl = QLabel(label)
        lbl.setStyleSheet("color: #9cdcfe; font-size: 12px; min-width: 100px;")

        cb = QComboBox()
        cb.addItems(items)
        if value in items:
            cb.setCurrentText(value)
        cb.setStyleSheet("""
            QComboBox {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #4c4c4c;
                border-radius: 3px;
                padding: 4px 6px;
                font-size: 12px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid #888;
            }
        """)
        cb.currentTextChanged.connect(lambda text, n=name: self.changed.emit(n, text))

        layout.addWidget(lbl)
        layout.addWidget(cb)
        self.content_layout.addWidget(w)
        return cb

    def add_spinbox(self, name, label, value=0, min_val=0, max_val=999):
        """Добавляет числовое поле"""
        w = QWidget()
        layout = QHBoxLayout(w)
        layout.setContentsMargins(0, 0, 0, 0)

        lbl = QLabel(label)
        lbl.setStyleSheet("color: #9cdcfe; font-size: 12px; min-width: 100px;")

        sb = QSpinBox()
        sb.setRange(min_val, max_val)
        sb.setValue(value)
        sb.setStyleSheet("""
            QSpinBox {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #4c4c4c;
                border-radius: 3px;
                padding: 4px 6px;
                font-size: 12px;
            }
        """)
        sb.valueChanged.connect(lambda val, n=name: self.changed.emit(n, val))

        layout.addWidget(lbl)
        layout.addWidget(sb)
        self.content_layout.addWidget(w)
        return sb

    def add_textedit(self, name, label, value=""):
        """Добавляет многострочное поле ввода"""
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(0, 0, 0, 0)

        lbl = QLabel(label)
        lbl.setStyleSheet("color: #9cdcfe; font-size: 12px;")

        te = QTextEdit()
        te.setPlainText(value)
        te.setMinimumHeight(80)
        te.setStyleSheet("""
            QTextEdit {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #4c4c4c;
                border-radius: 3px;
                padding: 4px;
                font-size: 12px;
            }
        """)
        te.textChanged.connect(lambda: self.changed.emit(name, te.toPlainText()))

        layout.addWidget(lbl)
        layout.addWidget(te)
        self.content_layout.addWidget(w)
        return te

    def add_button(self, label, callback):
        """Добавляет кнопку"""
        btn = QPushButton(label)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #0e639c;
                color: white;
                border: none;
                padding: 6px;
                border-radius: 3px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1177bb;
            }
        """)
        btn.clicked.connect(callback)
        self.content_layout.addWidget(btn)
        return btn


class PropertyPanel(QWidget):
    """
    Панель свойств для конструктора таблиц
    """

    propertyChanged = pyqtSignal(str, object)  # имя свойства, новое значение

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_field = None
        self.current_table = None
        self.sections = []
        self.setup_ui()

    def setup_ui(self):
        """Создание интерфейса панели"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.setSpacing(0)

        # Верхняя панель с заголовком
        title_bar = QWidget()
        title_bar.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                border-bottom: 1px solid #3c3c3c;
            }
        """)
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(8, 8, 8, 8)

        self.title_label = QLabel("СВОЙСТВА")
        self.title_label.setStyleSheet("color: #4ec9b0; font-weight: bold; font-size: 12px;")

        self.object_label = QLabel("")
        self.object_label.setStyleSheet("color: #9cdcfe; font-size: 11px;")

        title_layout.addWidget(self.title_label)
        title_layout.addStretch()
        title_layout.addWidget(self.object_label)

        layout.addWidget(title_bar)

        # Область прокрутки для свойств
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("""
            QScrollArea {
                background-color: #252526;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #2d2d2d;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #4c4c4c;
                border-radius: 6px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #5c5c5c;
            }
        """)

        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(8, 8, 8, 8)
        self.content_layout.setSpacing(12)
        self.content_layout.addStretch()

        scroll.setWidget(self.content)
        layout.addWidget(scroll)

    def clear(self):
        """Очищает панель свойств"""
        while self.content_layout.count() > 1:
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.sections.clear()
        self.object_label.setText("")

    def set_field(self, field_data):
        """Устанавливает поле для отображения свойств"""
        self.clear()
        self.current_field = field_data

        # Определяем тип поля
        field_type = field_data.get('type', 'TEXT')
        if hasattr(field_type, 'value'):
            field_type = field_type.value

        type_names = {
            'TEXT': 'Текст',
            'TEXT_MULTILINE': 'Многострочный текст',
            'INTEGER': 'Целое число',
            'FLOAT': 'Дробное число',
            'DATE': 'Дата',
            'TIME': 'Время',
            'DATETIME': 'Дата и время',
            'BOOLEAN': 'Да/Нет',
            'LIST': 'Список',
            'REFERENCE': 'Ссылка',
            'PHONE': 'Телефон',
            'EMAIL': 'Email',
            'MONEY': 'Деньги',
            'PERCENT': 'Процент',
            'FILE': 'Файл',
            'IMAGE': 'Изображение',
            'COLOR': 'Цвет',
            'RATING': 'Рейтинг',
            'CALCULATED': 'Вычисляемое',
        }
        type_name = type_names.get(field_type, field_type)
        self.object_label.setText(f"{type_name} • {field_data.get('display_name', '')}")

        # ===== ОСНОВНЫЕ СВОЙСТВА =====
        main_section = PropertySection("ОСНОВНЫЕ")
        main_section.changed.connect(self.propertyChanged.emit)

        main_section.add_checkbox("required", "Обязательное поле", field_data.get('required', False))
        main_section.add_checkbox("unique", "Уникальное значение", field_data.get('unique', False))
        main_section.add_lineedit("default", "По умолчанию", field_data.get('default', ''))
        main_section.add_lineedit("description", "Подсказка", field_data.get('description', ''))

        self.content_layout.insertWidget(self.content_layout.count() - 1, main_section)
        self.sections.append(main_section)

        # ===== СПЕЦИФИЧЕСКИЕ СВОЙСТВА =====
        if field_type == 'TEXT':
            self._add_text_properties(field_data)
        elif field_type == 'TEXT_MULTILINE':
            self._add_multiline_properties(field_data)
        elif field_type in ['INTEGER', 'FLOAT', 'MONEY', 'PERCENT']:
            self._add_number_properties(field_data)
        elif field_type == 'DATE':
            self._add_date_properties(field_data)
        elif field_type == 'LIST':
            self._add_list_properties(field_data)
        elif field_type == 'REFERENCE':
            self._add_reference_properties(field_data)
        elif field_type == 'CALCULATED':
            self._add_calculated_properties(field_data)

    def _add_text_properties(self, field_data):
        """Свойства для текстового поля"""
        section = PropertySection("ФОРМАТ ТЕКСТА")
        section.changed.connect(self.propertyChanged.emit)

        formats = [
            "Как написано",
            "Первая прописная",
            "ВСЕ ПРОПИСНЫЕ",
            "все строчные",
            "Каждое Слово С Большой"
        ]
        section.add_combobox("text_format", "Формат:", field_data.get('text_format', 'Как написано'), formats)
        section.add_spinbox("max_length", "Макс. длина:", field_data.get('max_length', 255), 1, 65535)

        self.content_layout.insertWidget(self.content_layout.count() - 1, section)
        self.sections.append(section)

    def _add_multiline_properties(self, field_data):
        """Свойства для многострочного текста"""
        section = PropertySection("ФОРМАТ ТЕКСТА")
        section.changed.connect(self.propertyChanged.emit)

        formats = ["Обычный текст", "RTF", "HTML", "Markdown"]
        section.add_combobox("multiline_format", "Формат:", field_data.get('multiline_format', 'Обычный текст'), formats)
        section.add_spinbox("height", "Высота (строк):", field_data.get('height', 5), 1, 50)
        section.add_checkbox("word_wrap", "Перенос по словам", field_data.get('word_wrap', True))

        self.content_layout.insertWidget(self.content_layout.count() - 1, section)
        self.sections.append(section)

    def _add_number_properties(self, field_data):
        """Свойства для чисел"""
        section = PropertySection("ФОРМАТ ЧИСЛА")
        section.changed.connect(self.propertyChanged.emit)

        field_type = field_data.get('type', 'INTEGER')
        if hasattr(field_type, 'value'):
            field_type = field_type.value

        if field_type == 'MONEY':
            currencies = ["₽ (Рубль)", "$ (Доллар)", "€ (Евро)", "₸ (Тенге)"]
            section.add_combobox("currency", "Валюта:", field_data.get('currency', '₽ (Рубль)'), currencies)
            section.add_spinbox("decimals", "Знаков после запятой:", field_data.get('decimals', 2), 0, 10)
        elif field_type == 'PERCENT':
            section.add_checkbox("show_percent_sign", "Показывать знак %", field_data.get('show_percent_sign', True))
            section.add_spinbox("decimals", "Знаков после запятой:", field_data.get('decimals', 1), 0, 10)

        section.add_spinbox("min_value", "Минимум:", field_data.get('min_value', 0), -999999, 999999)
        section.add_spinbox("max_value", "Максимум:", field_data.get('max_value', 100), -999999, 999999)
        section.add_checkbox("use_thousands", "Разделитель тысяч", field_data.get('use_thousands', False))

        self.content_layout.insertWidget(self.content_layout.count() - 1, section)
        self.sections.append(section)

    def _add_date_properties(self, field_data):
        """Свойства для даты"""
        section = PropertySection("ФОРМАТ ДАТЫ")
        section.changed.connect(self.propertyChanged.emit)

        date_formats = [
            "ДД.ММ.ГГГГ",
            "ММ.ДД.ГГГГ",
            "ГГГГ-ММ-ДД",
            "ДД месяц ГГГГ",
            "день недели, ДД месяц ГГГГ",
            "ММ/ГГГГ",
            "ГГГГ"
        ]
        section.add_combobox("date_format", "Формат даты:", field_data.get('date_format', 'ДД.ММ.ГГГГ'), date_formats)

        time_formats = ["Без времени", "ЧЧ:ММ", "ЧЧ:ММ:СС", "ЧЧ:ММ AM/PM"]
        section.add_combobox("time_format", "Формат времени:", field_data.get('time_format', 'Без времени'), time_formats)

        section.add_checkbox("auto_current", "Автоматически текущая дата", field_data.get('auto_current', False))

        self.content_layout.insertWidget(self.content_layout.count() - 1, section)
        self.sections.append(section)

    def _add_list_properties(self, field_data):
        """Свойства для списка"""
        section = PropertySection("ЭЛЕМЕНТЫ СПИСКА")
        section.changed.connect(self.propertyChanged.emit)

        options = field_data.get('options', [])
        options_str = '\n'.join(options) if options else ''
        section.add_textedit("list_options", "Варианты (по одному в строке):", options_str)

        list_types = ["Выпадающий список", "Переключатели", "Флажки (множественный выбор)"]
        section.add_combobox("list_type", "Вид:", field_data.get('list_type', 'Выпадающий список'), list_types)

        sort_types = ["Как введено", "По алфавиту", "По алфавиту (обратный)"]
        section.add_combobox("sort_type", "Сортировка:", field_data.get('sort_type', 'Как введено'), sort_types)

        self.content_layout.insertWidget(self.content_layout.count() - 1, section)
        self.sections.append(section)

    def _add_reference_properties(self, field_data):
        """Свойства для ссылки на таблицу"""
        section = PropertySection("СВЯЗЬ С ТАБЛИЦЕЙ")
        section.changed.connect(self.propertyChanged.emit)

        tables = ["Клиенты", "Товары", "Заказы", "Сотрудники"]  # TODO: получать из ProjectManager
        section.add_combobox("reference_table", "Таблица:", field_data.get('reference_table', ''), tables)

        fields = ["id", "Название"]  # TODO: получать из ProjectManager
        section.add_combobox("reference_display", "Показывать поле:", field_data.get('reference_display', ''), fields)

        relation_types = ["Одна запись", "Несколько записей (множественный выбор)"]
        section.add_combobox("relation_type", "Тип связи:", field_data.get('relation_type', 'Одна запись'), relation_types)

        self.content_layout.insertWidget(self.content_layout.count() - 1, section)
        self.sections.append(section)

    def _add_calculated_properties(self, field_data):
        """Свойства для вычисляемого поля"""
        section = PropertySection("ВЫЧИСЛЯЕМОЕ ПОЛЕ")
        section.changed.connect(self.propertyChanged.emit)

        def open_formula_editor():
            from ..dialogs.formula_dialog import FormulaDialog
            dialog = FormulaDialog(self, field_data.get('formula', ''))
            if dialog.exec() == QDialog.DialogCode.Accepted:
                formula = dialog.get_formula()
                self.propertyChanged.emit('formula', formula)

        section.add_button("🧮 РЕДАКТОР ФОРМУЛ", open_formula_editor)

        self.formula_preview = QLabel(field_data.get('formula', 'Формула не задана'))
        self.formula_preview.setStyleSheet("""
            QLabel {
                background-color: #2d2d2d;
                color: #ce9178;
                border: 1px solid #4c4c4c;
                border-radius: 3px;
                padding: 8px;
                font-family: monospace;
                font-size: 12px;
                min-height: 40px;
            }
        """)
        self.formula_preview.setWordWrap(True)

        preview_container = QWidget()
        preview_layout = QVBoxLayout(preview_container)
        preview_layout.setContentsMargins(0, 0, 0, 0)
        preview_layout.addWidget(QLabel("Текущая формула:"))
        preview_layout.addWidget(self.formula_preview)

        section.content_layout.addWidget(preview_container)

        result_types = ["Текст", "Число", "Дата", "Логический"]
        section.add_combobox("result_type", "Тип результата:", field_data.get('result_type', 'Текст'), result_types)

        self.content_layout.insertWidget(self.content_layout.count() - 1, section)
        self.sections.append(section)

    def set_table(self, table_data):
        """Устанавливает таблицу для отображения свойств"""
        self.clear()
        self.current_table = table_data
        self.object_label.setText(f"ТАБЛИЦА • {table_data.get('display_name', '')}")

        section = PropertySection("СВОЙСТВА ТАБЛИЦЫ")
        section.changed.connect(self.propertyChanged.emit)

        section.add_lineedit("display_name", "Название:", table_data.get('display_name', ''))
        section.add_lineedit("description", "Описание:", table_data.get('description', ''))
        section.add_lineedit("icon", "Иконка:", table_data.get('icon', '📊'))

        # Цвет
        color_widget = QWidget()
        color_layout = QHBoxLayout(color_widget)
        color_layout.setContentsMargins(0, 0, 0, 0)

        color_label = QLabel("Цвет:")
        color_label.setStyleSheet("color: #9cdcfe; font-size: 12px; min-width: 100px;")

        color_btn = QPushButton()
        color_btn.setFixedSize(24, 24)
        current_color = table_data.get('color', '#3b82f6')
        color_btn.setStyleSheet(f"background-color: {current_color}; border: 1px solid #4c4c4c; border-radius: 4px;")

        def pick_color():
            color = QColorDialog.getColor(QColor(current_color))
            if color.isValid():
                hex_color = color.name()
                color_btn.setStyleSheet(f"background-color: {hex_color}; border: 1px solid #4c4c4c; border-radius: 4px;")
                self.propertyChanged.emit('color', hex_color)

        color_btn.clicked.connect(pick_color)

        color_layout.addWidget(color_label)
        color_layout.addWidget(color_btn)
        color_layout.addStretch()

        section.content_layout.addWidget(color_widget)
        section.add_checkbox("protected", "Защитить от изменений", table_data.get('protected', False))

        self.content_layout.insertWidget(self.content_layout.count() - 1, section)
        self.sections.append(section)