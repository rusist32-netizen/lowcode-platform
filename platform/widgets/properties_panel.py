# -*- coding: utf-8 -*-

"""
Панель свойств поля - МАКСИМАЛЬНЫЙ ФУНКЦИОНАЛ
"""

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from platform.core.field_types import FieldType


class PropertiesPanel(QWidget):
    """Панель свойств поля - ВСЕ ВОЗМОЖНЫЕ НАСТРОЙКИ"""
    
    propertiesChanged = pyqtSignal(dict)
    openFormulaEditor = pyqtSignal()
    
    def __init__(self, tables_list=None, parent=None):
        super().__init__(parent)
        
        self.tables_list = tables_list or []
        self.current_field = None
        self.current_table_id = None
        
        self.setMinimumHeight(400)
        self.setMaximumHeight(600)
        self.setStyleSheet("""
            QWidget {
                background-color: #1e293b;
                border-top: 1px solid #334155;
            }
            QGroupBox {
                color: #3b82f6;
                font-weight: 500;
                border: 1px solid #334155;
                border-radius: 4px;
                margin-top: 10px;
                font-size: 12px;
                background-color: #0f172a;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px;
            }
            QCheckBox {
                color: #e2e8f0;
                font-size: 12px;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QLabel {
                color: #94a3b8;
                font-size: 12px;
            }
            QComboBox {
                background-color: #0f172a;
                color: #e2e8f0;
                border: 1px solid #334155;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 12px;
                min-height: 28px;
            }
            QComboBox:hover {
                border: 1px solid #3b82f6;
            }
            QComboBox::drop-down {
                border: none;
                width: 24px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #3b82f6;
            }
            QLineEdit, QSpinBox, QDoubleSpinBox {
                background-color: #0f172a;
                color: #e2e8f0;
                border: 1px solid #334155;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 12px;
                min-height: 28px;
            }
            QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {
                border: 1px solid #3b82f6;
            }
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 12px;
                font-weight: 500;
                min-height: 32px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QPushButton.secondary {
                background-color: #475569;
            }
            QPushButton.secondary:hover {
                background-color: #64748b;
            }
            QPushButton.success {
                background-color: #10b981;
            }
            QPushButton.success:hover {
                background-color: #059669;
            }
            QTextEdit {
                background-color: #0f172a;
                color: #e2e8f0;
                border: 1px solid #334155;
                border-radius: 4px;
                padding: 4px;
                font-size: 12px;
                font-family: monospace;
            }
        """)
        
        self._setup_ui()
    
    def _setup_ui(self):
        # Главный layout с прокруткой
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Область с прокруткой
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
        
        # Контейнер для всего содержимого
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # ===== ЗАГОЛОВОК =====
        title_layout = QHBoxLayout()
        title_layout.setSpacing(8)
        
        title_icon = QLabel("⚙️")
        title_icon.setStyleSheet("font-size: 20px;")
        title_layout.addWidget(title_icon)
        
        title_label = QLabel("СВОЙСТВА ПОЛЯ")
        title_label.setStyleSheet("color: #3b82f6; font-size: 16px; font-weight: bold;")
        title_layout.addWidget(title_label)
        
        title_layout.addStretch()
        
        self.field_type_badge = QLabel("")
        self.field_type_badge.setStyleSheet("""
            background-color: #10b981;
            color: white;
            font-size: 11px;
            font-weight: bold;
            padding: 4px 12px;
            border-radius: 20px;
        """)
        self.field_type_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.addWidget(self.field_type_badge)
        
        layout.addLayout(title_layout)
        
        # ===== ОСНОВНЫЕ НАСТРОЙКИ =====
        basic_group = QGroupBox("Основные настройки")
        basic_layout = QVBoxLayout(basic_group)
        basic_layout.setSpacing(12)
        
        # Первая строка: Обязательное и Уникальное
        row1 = QHBoxLayout()
        row1.setSpacing(20)
        
        self.required_check = QCheckBox("Обязательное поле")
        self.required_check.setFixedHeight(24)
        row1.addWidget(self.required_check)
        
        self.unique_check = QCheckBox("Уникальное значение")
        self.unique_check.setFixedHeight(24)
        row1.addWidget(self.unique_check)
        
        row1.addStretch()
        basic_layout.addLayout(row1)
        
        # Вторая строка: Значение по умолчанию
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Значение по умолчанию:"), 1)
        
        self.default_edit = QLineEdit()
        self.default_edit.setPlaceholderText("например: 0, Да, Текст, 01.01.2024")
        self.default_edit.setFixedHeight(32)
        row2.addWidget(self.default_edit, 2)
        
        basic_layout.addLayout(row2)
        
        layout.addWidget(basic_group)
        
        # ===== НАСТРОЙКИ ФОРМАТИРОВАНИЯ =====
        self.format_group = QGroupBox("Форматирование")
        self.format_layout = QVBoxLayout(self.format_group)
        self.format_layout.setSpacing(12)
        
        # Стек для разных типов форматирования
        self.format_stack = QStackedWidget()
        self.format_stack.setMinimumHeight(200)
        
        # Пустая страница
        self.format_stack.addWidget(QWidget())
        
        # Страница для текста
        self.text_widget = self._create_text_widget()
        self.format_stack.addWidget(self.text_widget)
        
        # Страница для чисел
        self.number_widget = self._create_number_widget()
        self.format_stack.addWidget(self.number_widget)
        
        # Страница для даты
        self.date_widget = self._create_date_widget()
        self.format_stack.addWidget(self.date_widget)
        
        # Страница для времени
        self.time_widget = self._create_time_widget()
        self.format_stack.addWidget(self.time_widget)
        
        # Страница для даты и времени
        self.datetime_widget = self._create_datetime_widget()
        self.format_stack.addWidget(self.datetime_widget)
        
        # Страница для денег
        self.money_widget = self._create_money_widget()
        self.format_stack.addWidget(self.money_widget)
        
        # Страница для процентов
        self.percent_widget = self._create_percent_widget()
        self.format_stack.addWidget(self.percent_widget)
        
        # Страница для логических значений
        self.boolean_widget = self._create_boolean_widget()
        self.format_stack.addWidget(self.boolean_widget)
        
        # Страница для телефона
        self.phone_widget = self._create_phone_widget()
        self.format_stack.addWidget(self.phone_widget)
        
        # Страница для email
        self.email_widget = self._create_email_widget()
        self.format_stack.addWidget(self.email_widget)
        
        # Страница для URL
        self.url_widget = self._create_url_widget()
        self.format_stack.addWidget(self.url_widget)
        
        self.format_layout.addWidget(self.format_stack)
        layout.addWidget(self.format_group)
        
        # ===== СВЯЗЬ С ДРУГИМИ ТАБЛИЦАМИ =====
        self.reference_group = QGroupBox("Связь с таблицей")
        self.reference_group.setVisible(False)
        ref_layout = QVBoxLayout(self.reference_group)
        ref_layout.setSpacing(12)
        
        # Выбор таблицы
        ref_row1 = QHBoxLayout()
        ref_row1.addWidget(QLabel("Таблица:"), 1)
        
        self.reference_table_combo = QComboBox()
        self.reference_table_combo.setFixedHeight(32)
        self.reference_table_combo.currentIndexChanged.connect(self._on_reference_table_changed)
        ref_row1.addWidget(self.reference_table_combo, 2)
        ref_layout.addLayout(ref_row1)
        
        # Поле для отображения
        ref_row2 = QHBoxLayout()
        ref_row2.addWidget(QLabel("Показывать поле:"), 1)
        
        self.reference_display_combo = QComboBox()
        self.reference_display_combo.setFixedHeight(32)
        self.reference_display_combo.currentIndexChanged.connect(self._on_property_changed)
        ref_row2.addWidget(self.reference_display_combo, 2)
        ref_layout.addLayout(ref_row2)
        
        # Условие фильтрации
        ref_row3 = QHBoxLayout()
        ref_row3.addWidget(QLabel("Фильтр:"), 1)
        
        self.reference_filter_edit = QLineEdit()
        self.reference_filter_edit.setPlaceholderText("например: status = 'active'")
        self.reference_filter_edit.setFixedHeight(32)
        self.reference_filter_edit.textChanged.connect(self._on_property_changed)
        ref_row3.addWidget(self.reference_filter_edit, 2)
        ref_layout.addLayout(ref_row3)
        
        # Сортировка
        ref_row4 = QHBoxLayout()
        ref_row4.addWidget(QLabel("Сортировка:"), 1)
        
        self.reference_sort_combo = QComboBox()
        self.reference_sort_combo.setFixedHeight(32)
        self.reference_sort_combo.addItems(["По возрастанию", "По убыванию"])
        self.reference_sort_combo.currentIndexChanged.connect(self._on_property_changed)
        ref_row4.addWidget(self.reference_sort_combo, 2)
        ref_layout.addLayout(ref_row4)
        
        layout.addWidget(self.reference_group)
        
        # ===== ВЫЧИСЛЯЕМЫЕ ПОЛЯ =====
        self.formula_group = QGroupBox("Вычисляемое поле")
        self.formula_group.setVisible(False)
        formula_layout = QVBoxLayout(self.formula_group)
        formula_layout.setSpacing(12)
        
        # Кнопка открытия редактора формул
        self.formula_btn = QPushButton("🧮 Открыть визуальный редактор формул")
        self.formula_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.formula_btn.setFixedHeight(40)
        self.formula_btn.clicked.connect(self._open_formula_editor)
        formula_layout.addWidget(self.formula_btn)
        
        # Предпросмотр формулы
        preview_group = QWidget()
        preview_group.setStyleSheet("background-color: #0f172a; border: 1px solid #334155; border-radius: 4px;")
        preview_layout = QVBoxLayout(preview_group)
        preview_layout.setContentsMargins(8, 8, 8, 8)
        preview_layout.setSpacing(5)
        
        preview_layout.addWidget(QLabel("Текущая формула:"))
        
        self.formula_preview = QTextEdit()
        self.formula_preview.setReadOnly(True)
        self.formula_preview.setMaximumHeight(80)
        self.formula_preview.setPlaceholderText("Формула не задана")
        preview_layout.addWidget(self.formula_preview)
        
        formula_layout.addWidget(preview_group)
        
        # Настройки кэширования
        self.formula_cache_check = QCheckBox("Кэшировать результат")
        self.formula_cache_check.setChecked(True)
        self.formula_cache_check.toggled.connect(self._on_property_changed)
        formula_layout.addWidget(self.formula_cache_check)
        
        layout.addWidget(self.formula_group)
        
        # ===== ДОПОЛНИТЕЛЬНЫЕ НАСТРОЙКИ =====
        self.advanced_group = QGroupBox("Дополнительно")
        self.advanced_group.setVisible(False)
        advanced_layout = QVBoxLayout(self.advanced_group)
        advanced_layout.setSpacing(12)
        
        # Валидация
        adv_row1 = QHBoxLayout()
        adv_row1.addWidget(QLabel("Регулярное выражение:"), 1)
        
        self.regex_edit = QLineEdit()
        self.regex_edit.setPlaceholderText("например: ^[A-Z0-9]+$")
        self.regex_edit.setFixedHeight(32)
        self.regex_edit.textChanged.connect(self._on_property_changed)
        adv_row1.addWidget(self.regex_edit, 2)
        advanced_layout.addLayout(adv_row1)
        
        # Минимум и максимум
        range_layout = QHBoxLayout()
        range_layout.setSpacing(10)
        
        range_layout.addWidget(QLabel("Мин:"), 0)
        self.min_edit = QLineEdit()
        self.min_edit.setPlaceholderText("мин")
        self.min_edit.setFixedHeight(32)
        self.min_edit.setFixedWidth(80)
        self.min_edit.textChanged.connect(self._on_property_changed)
        range_layout.addWidget(self.min_edit)
        
        range_layout.addWidget(QLabel("Макс:"), 0)
        self.max_edit = QLineEdit()
        self.max_edit.setPlaceholderText("макс")
        self.max_edit.setFixedHeight(32)
        self.max_edit.setFixedWidth(80)
        self.max_edit.textChanged.connect(self._on_property_changed)
        range_layout.addWidget(self.max_edit)
        
        range_layout.addStretch()
        advanced_layout.addLayout(range_layout)
        
        layout.addWidget(self.advanced_group)
        
        # ===== КНОПКИ УПРАВЛЕНИЯ =====
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        self.reset_btn = QPushButton("Сбросить")
        self.reset_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.reset_btn.setProperty("class", "secondary")
        self.reset_btn.setFixedHeight(36)
        self.reset_btn.clicked.connect(self._reset_properties)
        btn_layout.addWidget(self.reset_btn)
        
        btn_layout.addStretch()
        
        self.apply_btn = QPushButton("Применить изменения")
        self.apply_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.apply_btn.setProperty("class", "success")
        self.apply_btn.setFixedHeight(40)
        self.apply_btn.setFixedWidth(180)
        self.apply_btn.clicked.connect(self._apply_properties)
        btn_layout.addWidget(self.apply_btn)
        
        layout.addLayout(btn_layout)
        
        # Растяжка в конце
        layout.addStretch()
        
        scroll.setWidget(content)
        main_layout.addWidget(scroll)
    
    def _create_text_widget(self) -> QWidget:
        """Виджет для текстовых полей"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        # Регистр
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Регистр:"), 1)
        
        self.text_case_combo = QComboBox()
        self.text_case_combo.setFixedHeight(32)
        self.text_case_combo.addItems([
            "Как введено",
            "ВСЕ ПРОПИСНЫЕ",
            "все строчные",
            "Первая буква прописная",
            "Каждое Слово С Заглавной"
        ])
        row1.addWidget(self.text_case_combo, 2)
        layout.addLayout(row1)
        
        # Максимальная длина
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Макс. длина:"), 1)
        
        self.text_maxlength_spin = QSpinBox()
        self.text_maxlength_spin.setRange(0, 10000)
        self.text_maxlength_spin.setValue(0)
        self.text_maxlength_spin.setSpecialValueText("Без ограничений")
        self.text_maxlength_spin.setFixedHeight(32)
        row2.addWidget(self.text_maxlength_spin, 2)
        layout.addLayout(row2)
        
        # Дополнительные опции
        self.text_trim_check = QCheckBox("Удалять лишние пробелы")
        self.text_trim_check.setFixedHeight(24)
        layout.addWidget(self.text_trim_check)
        
        self.text_multiline_check = QCheckBox("Многострочный режим")
        self.text_multiline_check.setFixedHeight(24)
        layout.addWidget(self.text_multiline_check)
        
        return widget
    
    def _create_number_widget(self) -> QWidget:
        """Виджет для числовых полей"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        # Формат числа
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Формат:"), 1)
        
        self.number_format_combo = QComboBox()
        self.number_format_combo.setFixedHeight(32)
        self.number_format_combo.addItems([
            "Обычный",
            "С разделителями тысяч",
            "Научный (1.23E+4)",
            "Денежный"
        ])
        row1.addWidget(self.number_format_combo, 2)
        layout.addLayout(row1)
        
        # Знаков после запятой
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Знаков после запятой:"), 1)
        
        self.number_decimals_spin = QSpinBox()
        self.number_decimals_spin.setRange(0, 10)
        self.number_decimals_spin.setValue(2)
        self.number_decimals_spin.setFixedHeight(32)
        row2.addWidget(self.number_decimals_spin, 2)
        layout.addLayout(row2)
        
        # Отрицательные числа
        self.number_neg_parens_check = QCheckBox("Отрицательные числа в скобках")
        self.number_neg_parens_check.setFixedHeight(24)
        layout.addWidget(self.number_neg_parens_check)
        
        self.number_neg_red_check = QCheckBox("Отрицательные числа красным")
        self.number_neg_red_check.setFixedHeight(24)
        layout.addWidget(self.number_neg_red_check)
        
        return widget
    
    def _create_date_widget(self) -> QWidget:
        """Виджет для полей даты"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        # Формат даты
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Формат:"), 1)
        
        self.date_format_combo = QComboBox()
        self.date_format_combo.setFixedHeight(32)
        self.date_format_combo.addItems([
            "ДД.ММ.ГГГГ",
            "ДД.ММ.ГГ",
            "ГГГГ-ММ-ДД",
            "ДД/ММ/ГГГГ",
            "ДД месяц ГГГГ",
            "месяц ГГГГ",
            "ДД месяц",
            "месяц",
            "ГГГГ"
        ])
        row1.addWidget(self.date_format_combo, 2)
        layout.addLayout(row1)
        
        return widget
    
    def _create_time_widget(self) -> QWidget:
        """Виджет для полей времени"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Формат:"), 1)
        
        self.time_format_combo = QComboBox()
        self.time_format_combo.setFixedHeight(32)
        self.time_format_combo.addItems([
            "ЧЧ:ММ:СС",
            "ЧЧ:ММ",
            "ЧЧ:ММ AM/PM",
            "ЧЧ:ММ:СС AM/PM"
        ])
        row1.addWidget(self.time_format_combo, 2)
        layout.addLayout(row1)
        
        return widget
    
    def _create_datetime_widget(self) -> QWidget:
        """Виджет для полей даты и времени"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Формат:"), 1)
        
        self.datetime_format_combo = QComboBox()
        self.datetime_format_combo.setFixedHeight(32)
        self.datetime_format_combo.addItems([
            "ДД.ММ.ГГГГ ЧЧ:ММ",
            "ДД.ММ.ГГГГ ЧЧ:ММ:СС",
            "ГГГГ-ММ-ДД ЧЧ:ММ",
            "ДД/ММ/ГГГГ ЧЧ:ММ"
        ])
        row1.addWidget(self.datetime_format_combo, 2)
        layout.addLayout(row1)
        
        return widget
    
    def _create_money_widget(self) -> QWidget:
        """Виджет для денежных полей"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        # Валюта
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Валюта:"), 1)
        
        self.money_currency_combo = QComboBox()
        self.money_currency_combo.setFixedHeight(32)
        self.money_currency_combo.addItems([
            "Рубли (₽)",
            "Доллары ($)",
            "Евро (€)",
            "Фунты (£)",
            "Йены (¥)",
            "Юани (¥)"
        ])
        row1.addWidget(self.money_currency_combo, 2)
        layout.addLayout(row1)
        
        # Знаков после запятой
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Знаков после запятой:"), 1)
        
        self.money_decimals_spin = QSpinBox()
        self.money_decimals_spin.setRange(0, 4)
        self.money_decimals_spin.setValue(2)
        self.money_decimals_spin.setFixedHeight(32)
        row2.addWidget(self.money_decimals_spin, 2)
        layout.addLayout(row2)
        
        # Разделитель тысяч
        self.money_thousands_check = QCheckBox("Использовать разделитель тысяч")
        self.money_thousands_check.setChecked(True)
        self.money_thousands_check.setFixedHeight(24)
        layout.addWidget(self.money_thousands_check)
        
        return widget
    
    def _create_percent_widget(self) -> QWidget:
        """Виджет для процентов"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Формат:"), 1)
        
        self.percent_format_combo = QComboBox()
        self.percent_format_combo.setFixedHeight(32)
        self.percent_format_combo.addItems([
            "12.34%",
            "0.1234",
            "12.34 п.п."
        ])
        row1.addWidget(self.percent_format_combo, 2)
        layout.addLayout(row1)
        
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Знаков:"), 1)
        
        self.percent_decimals_spin = QSpinBox()
        self.percent_decimals_spin.setRange(0, 6)
        self.percent_decimals_spin.setValue(2)
        self.percent_decimals_spin.setFixedHeight(32)
        row2.addWidget(self.percent_decimals_spin, 2)
        layout.addLayout(row2)
        
        return widget
    
    def _create_boolean_widget(self) -> QWidget:
        """Виджет для логических полей"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Отображение:"), 1)
        
        self.boolean_format_combo = QComboBox()
        self.boolean_format_combo.setFixedHeight(32)
        self.boolean_format_combo.addItems([
            "Да/Нет",
            "True/False",
            "Вкл/Выкл",
            "✓/✗",
            "✅/❌",
            "1/0"
        ])
        row1.addWidget(self.boolean_format_combo, 2)
        layout.addLayout(row1)
        
        # Пользовательские значения
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Истина:"), 1)
        
        self.boolean_true_edit = QLineEdit()
        self.boolean_true_edit.setPlaceholderText("Да")
        self.boolean_true_edit.setFixedHeight(32)
        row2.addWidget(self.boolean_true_edit, 2)
        layout.addLayout(row2)
        
        row3 = QHBoxLayout()
        row3.addWidget(QLabel("Ложь:"), 1)
        
        self.boolean_false_edit = QLineEdit()
        self.boolean_false_edit.setPlaceholderText("Нет")
        self.boolean_false_edit.setFixedHeight(32)
        row3.addWidget(self.boolean_false_edit, 2)
        layout.addLayout(row3)
        
        return widget
    
    def _create_phone_widget(self) -> QWidget:
        """Виджет для телефона"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Формат:"), 1)
        
        self.phone_format_combo = QComboBox()
        self.phone_format_combo.setFixedHeight(32)
        self.phone_format_combo.addItems([
            "+7 (999) 999-99-99",
            "8 (999) 999-99-99",
            "999-999-99-99",
            "(999) 999-9999"
        ])
        row1.addWidget(self.phone_format_combo, 2)
        layout.addLayout(row1)
        
        return widget
    
    def _create_email_widget(self) -> QWidget:
        """Виджет для email"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        self.email_lowercase_check = QCheckBox("Автоматически в нижний регистр")
        self.email_lowercase_check.setFixedHeight(24)
        layout.addWidget(self.email_lowercase_check)
        
        self.email_trim_check = QCheckBox("Удалять пробелы")
        self.email_trim_check.setChecked(True)
        self.email_trim_check.setFixedHeight(24)
        layout.addWidget(self.email_trim_check)
        
        return widget
    
    def _create_url_widget(self) -> QWidget:
        """Виджет для URL"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        self.url_protocol_check = QCheckBox("Добавлять https:// если не указано")
        self.url_protocol_check.setChecked(True)
        self.url_protocol_check.setFixedHeight(24)
        layout.addWidget(self.url_protocol_check)
        
        self.url_lowercase_check = QCheckBox("В нижний регистр")
        self.url_lowercase_check.setFixedHeight(24)
        layout.addWidget(self.url_lowercase_check)
        
        return widget
    
    def _open_formula_editor(self):
        """Открыть редактор формул"""
        self.openFormulaEditor.emit()
    
    def _on_reference_table_changed(self):
        """При изменении связанной таблицы"""
        self._update_display_fields()
        self._on_property_changed()
    
    def _update_display_fields(self):
        """Обновить список полей для отображения"""
        self.reference_display_combo.clear()
        
        table_id = self.reference_table_combo.currentData()
        if not table_id or not self.tables_list:
            return
        
        for table in self.tables_list:
            if table['id'] == table_id:
                for field in table.get('fields', []):
                    self.reference_display_combo.addItem(
                        field.get('name_ru', 'Без имени'),
                        field.get('id')
                    )
                break
    
    def set_tables(self, tables_list):
        """Сохранить список таблиц для ссылок"""
        self.tables_list = tables_list
        self._update_reference_tables()
    
    def set_current_table(self, table_id: str):
        """Установить ID текущей таблицы"""
        self.current_table_id = table_id
    
    def _update_reference_tables(self):
        """Обновить список доступных таблиц для ссылок"""
        self.reference_table_combo.clear()
        self.reference_table_combo.addItem("— выберите таблицу —", None)
        
        if not self.tables_list:
            return
        
        for table in self.tables_list:
            if table['id'] != self.current_table_id:
                self.reference_table_combo.addItem(
                    f"{table.get('icon', '📊')} {table['name_ru']}", 
                    table['id']
                )
    
    def set_field(self, field_data: dict = None):
        """Установка текущего поля и загрузка его свойств"""
        print(f"📋 Загрузка свойств для поля: {field_data.get('name_ru') if field_data else 'None'}")
        
        self.current_field = field_data
        
        if not field_data:
            self.field_type_badge.setText("")
            self.reference_group.setVisible(False)
            self.formula_group.setVisible(False)
            self.advanced_group.setVisible(False)
            self.format_group.setVisible(False)
            return
        
        field_type = field_data.get('type', 'Текст')
        self.field_type_badge.setText(field_type)
        
        # Показываем/скрываем группы в зависимости от типа
        self._update_visibility_by_type(field_type)
        
        # Загружаем основные настройки
        self.required_check.setChecked(field_data.get('required', False))
        self.unique_check.setChecked(field_data.get('unique', False))
        self.default_edit.setText(field_data.get('default', ''))
        
        # Загружаем настройки форматирования
        format_config = field_data.get('format', {})
        self._load_format_properties(field_type, format_config)
        
        # Загружаем настройки ссылок
        if FieldType.is_reference(field_type):
            ref_table = field_data.get('reference_table')
            if ref_table:
                index = self.reference_table_combo.findData(ref_table)
                if index >= 0:
                    self.reference_table_combo.setCurrentIndex(index)
            
            display_field = field_data.get('display_field')
            if display_field:
                index = self.reference_display_combo.findData(display_field)
                if index >= 0:
                    self.reference_display_combo.setCurrentIndex(index)
            
            self.reference_filter_edit.setText(field_data.get('reference_filter', ''))
        
        # Загружаем настройки вычисляемых полей
        if field_type == "Вычисляемое":
            formula = field_data.get('formula', '')
            if formula:
                self.formula_preview.setText(formula)
            else:
                self.formula_preview.setPlainText("Формула не задана")
            self.formula_cache_check.setChecked(field_data.get('cache_result', True))
        
        # Загружаем дополнительные настройки
        self.regex_edit.setText(field_data.get('validation_regex', ''))
        self.min_edit.setText(str(field_data.get('min_value', '')) if field_data.get('min_value') is not None else '')
        self.max_edit.setText(str(field_data.get('max_value', '')) if field_data.get('max_value') is not None else '')
    
    def _update_visibility_by_type(self, field_type: str):
        """Обновить видимость групп в зависимости от типа поля"""
        # Группа форматирования видна всегда, но с разной страницей
        self.format_group.setVisible(True)
        
        # Выбираем страницу в стеке
        if field_type == "Текст" or field_type == "Текст (многострочный)":
            self.format_stack.setCurrentIndex(1)
        elif field_type in ["Число целое", "Число дробное"]:
            self.format_stack.setCurrentIndex(2)
        elif field_type == "Дата":
            self.format_stack.setCurrentIndex(3)
        elif field_type == "Время":
            self.format_stack.setCurrentIndex(4)
        elif field_type == "Дата и время":
            self.format_stack.setCurrentIndex(5)
        elif field_type == "Деньги":
            self.format_stack.setCurrentIndex(6)
        elif field_type == "Процент":
            self.format_stack.setCurrentIndex(7)
        elif field_type == "Да/Нет":
            self.format_stack.setCurrentIndex(8)
        elif field_type == "Телефон":
            self.format_stack.setCurrentIndex(9)
        elif field_type == "Email":
            self.format_stack.setCurrentIndex(10)
        elif field_type == "URL":
            self.format_stack.setCurrentIndex(11)
        else:
            self.format_stack.setCurrentIndex(0)
        
        # Группа ссылок видна только для ссылочных типов
        self.reference_group.setVisible(FieldType.is_reference(field_type))
        
        # Группа вычисляемых полей
        self.formula_group.setVisible(field_type == "Вычисляемое")
        
        # Дополнительные настройки
        self.advanced_group.setVisible(True)
    
    def _load_format_properties(self, field_type: str, format_config: dict):
        """Загрузить настройки форматирования"""
        if field_type == "Текст" or field_type == "Текст (многострочный)":
            self.text_case_combo.setCurrentIndex(format_config.get('case', 0))
            self.text_maxlength_spin.setValue(format_config.get('max_length', 0))
            self.text_trim_check.setChecked(format_config.get('trim', False))
            self.text_multiline_check.setChecked(format_config.get('multiline', field_type == "Текст (многострочный)"))
            
        elif field_type in ["Число целое", "Число дробное"]:
            self.number_format_combo.setCurrentIndex(format_config.get('number_format', 0))
            self.number_decimals_spin.setValue(format_config.get('decimals', 2))
            self.number_neg_parens_check.setChecked(format_config.get('negative_parens', False))
            self.number_neg_red_check.setChecked(format_config.get('negative_red', False))
            
        elif field_type == "Дата":
            self.date_format_combo.setCurrentIndex(format_config.get('date_format', 0))
            
        elif field_type == "Время":
            self.time_format_combo.setCurrentIndex(format_config.get('time_format', 0))
            
        elif field_type == "Дата и время":
            self.datetime_format_combo.setCurrentIndex(format_config.get('datetime_format', 0))
            
        elif field_type == "Деньги":
            self.money_currency_combo.setCurrentIndex(format_config.get('currency', 0))
            self.money_decimals_spin.setValue(format_config.get('decimals', 2))
            self.money_thousands_check.setChecked(format_config.get('thousands', True))
            
        elif field_type == "Процент":
            self.percent_format_combo.setCurrentIndex(format_config.get('percent_format', 0))
            self.percent_decimals_spin.setValue(format_config.get('decimals', 2))
            
        elif field_type == "Да/Нет":
            self.boolean_format_combo.setCurrentIndex(format_config.get('boolean_format', 0))
            self.boolean_true_edit.setText(format_config.get('true_text', 'Да'))
            self.boolean_false_edit.setText(format_config.get('false_text', 'Нет'))
            
        elif field_type == "Телефон":
            self.phone_format_combo.setCurrentIndex(format_config.get('phone_format', 0))
            
        elif field_type == "Email":
            self.email_lowercase_check.setChecked(format_config.get('lowercase', False))
            self.email_trim_check.setChecked(format_config.get('trim', True))
            
        elif field_type == "URL":
            self.url_protocol_check.setChecked(format_config.get('add_protocol', True))
            self.url_lowercase_check.setChecked(format_config.get('lowercase', False))
    
    def _on_property_changed(self):
        """Свойство изменено"""
        pass
    
    def _reset_properties(self):
        """Сбросить все настройки к значениям по умолчанию"""
        if not self.current_field:
            return
        
        # Создаем пустой field_data с текущим типом
        empty_field = {
            'name_ru': self.current_field.get('name_ru', ''),
            'name_en': self.current_field.get('name_en', ''),
            'type': self.current_field.get('type', 'Текст'),
            'type_id': self.current_field.get('type_id', 'text'),
            'required': False,
            'unique': False,
            'default': None,
            'format': {}
        }
        
        self.set_field(empty_field)
    
    def _apply_properties(self):
        """Применить изменения свойств"""
        if not self.current_field:
            return
        
        print(f"📋 Применение свойств для: {self.current_field.get('name_ru')}")
        
        field_type = self.current_field.get('type', 'Текст')
        
        properties = {
            'required': self.required_check.isChecked(),
            'unique': self.unique_check.isChecked(),
            'default': self.default_edit.text() or None
        }
        
        # Сохраняем настройки форматирования
        format_config = self._get_format_config(field_type)
        if format_config:
            properties['format'] = format_config
        
        # Сохраняем настройки ссылок
        if FieldType.is_reference(field_type):
            properties['reference_table'] = self.reference_table_combo.currentData()
            properties['display_field'] = self.reference_display_combo.currentData()
            properties['reference_filter'] = self.reference_filter_edit.text() or None
        
        # Сохраняем настройки вычисляемых полей
        if field_type == "Вычисляемое":
            properties['formula'] = self.formula_preview.toPlainText() or None
            properties['cache_result'] = self.formula_cache_check.isChecked()
        
        # Сохраняем дополнительные настройки
        if self.regex_edit.text():
            properties['validation_regex'] = self.regex_edit.text()
        if self.min_edit.text():
            try:
                properties['min_value'] = float(self.min_edit.text())
            except:
                pass
        if self.max_edit.text():
            try:
                properties['max_value'] = float(self.max_edit.text())
            except:
                pass
        
        print(f"📋 Отправка сигнала с изменениями")
        self.propertiesChanged.emit(properties)
    
    def _get_format_config(self, field_type: str) -> dict:
        """Собрать настройки форматирования в зависимости от типа"""
        format_config = {}
        
        if field_type == "Текст" or field_type == "Текст (многострочный)":
            format_config = {
                'case': self.text_case_combo.currentIndex(),
                'max_length': self.text_maxlength_spin.value() or None,
                'trim': self.text_trim_check.isChecked(),
                'multiline': self.text_multiline_check.isChecked()
            }
            
        elif field_type in ["Число целое", "Число дробное"]:
            format_config = {
                'number_format': self.number_format_combo.currentIndex(),
                'decimals': self.number_decimals_spin.value(),
                'negative_parens': self.number_neg_parens_check.isChecked(),
                'negative_red': self.number_neg_red_check.isChecked()
            }
            
        elif field_type == "Дата":
            format_config = {
                'date_format': self.date_format_combo.currentIndex()
            }
            
        elif field_type == "Время":
            format_config = {
                'time_format': self.time_format_combo.currentIndex()
            }
            
        elif field_type == "Дата и время":
            format_config = {
                'datetime_format': self.datetime_format_combo.currentIndex()
            }
            
        elif field_type == "Деньги":
            format_config = {
                'currency': self.money_currency_combo.currentIndex(),
                'decimals': self.money_decimals_spin.value(),
                'thousands': self.money_thousands_check.isChecked()
            }
            
        elif field_type == "Процент":
            format_config = {
                'percent_format': self.percent_format_combo.currentIndex(),
                'decimals': self.percent_decimals_spin.value()
            }
            
        elif field_type == "Да/Нет":
            format_config = {
                'boolean_format': self.boolean_format_combo.currentIndex(),
                'true_text': self.boolean_true_edit.text() or 'Да',
                'false_text': self.boolean_false_edit.text() or 'Нет'
            }
            
        elif field_type == "Телефон":
            format_config = {
                'phone_format': self.phone_format_combo.currentIndex()
            }
            
        elif field_type == "Email":
            format_config = {
                'lowercase': self.email_lowercase_check.isChecked(),
                'trim': self.email_trim_check.isChecked()
            }
            
        elif field_type == "URL":
            format_config = {
                'add_protocol': self.url_protocol_check.isChecked(),
                'lowercase': self.url_lowercase_check.isChecked()
            }
        
        return format_config