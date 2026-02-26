#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Диалог редактора формул (no-code)
"""

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class FieldButton(QPushButton):
    """Кнопка для поля в формуле"""

    def __init__(self, field_name, field_data, parent=None):
        super().__init__(f"[{field_name}]", parent)
        self.field_name = field_name
        self.field_data = field_data
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background-color: #2d4f7c;
                color: white;
                border: 1px solid #3c6a9c;
                border-radius: 4px;
                padding: 6px 10px;
                font-size: 12px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #3c6a9c;
            }
        """)


class OperatorButton(QPushButton):
    """Кнопка оператора"""

    def __init__(self, operator, tooltip, parent=None):
        super().__init__(operator, parent)
        self.operator = operator
        self.setToolTip(tooltip)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(40, 40)
        self.setStyleSheet("""
            QPushButton {
                background-color: #4c4c4c;
                color: white;
                border: 1px solid #5c5c5c;
                border-radius: 4px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5c5c5c;
            }
        """)


class FunctionButton(QPushButton):
    """Кнопка функции"""

    def __init__(self, function, tooltip, parent=None):
        super().__init__(function, parent)
        self.function = function
        self.setToolTip(tooltip)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background-color: #8a6e3c;
                color: white;
                border: 1px solid #9a7e4c;
                border-radius: 4px;
                padding: 6px;
                font-size: 11px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #9a7e4c;
            }
        """)


class ConditionButton(QPushButton):
    """Кнопка условия"""

    def __init__(self, condition, tooltip, parent=None):
        super().__init__(condition, parent)
        self.condition = condition
        self.setToolTip(tooltip)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background-color: #8c4c4c;
                color: white;
                border: 1px solid #9c5c5c;
                border-radius: 4px;
                padding: 6px;
                font-size: 11px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #9c5c5c;
            }
        """)


class FormulaDialog(QDialog):
    """
    Диалог редактора формул
    Всё через перетаскивание и клики
    """

    def __init__(self, parent=None, initial_formula=""):
        super().__init__(parent)
        self.setWindowTitle("Редактор формул")
        self.setModal(True)
        self.setMinimumSize(900, 600)

        self.formula = initial_formula
        self.current_table = None
        self.fields = []  # поля текущей таблицы

        self.setup_ui()
        self.load_fields()

    def setup_ui(self):
        """Создание интерфейса диалога"""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # ===== ЛЕВАЯ ПАНЕЛЬ =====
        left_panel = QWidget()
        left_panel.setFixedWidth(250)
        left_panel.setStyleSheet("""
            QWidget {
                background-color: #252526;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
            }
        """)

        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(8, 8, 8, 8)
        left_layout.setSpacing(8)

        # Поля таблицы
        fields_label = QLabel("📋 ПОЛЯ ТАБЛИЦЫ")
        fields_label.setStyleSheet("color: #4ec9b0; font-weight: bold;")

        self.fields_scroll = QScrollArea()
        self.fields_scroll.setWidgetResizable(True)
        self.fields_scroll.setFrameShape(QFrame.Shape.NoFrame)

        self.fields_widget = QWidget()
        self.fields_layout = QVBoxLayout(self.fields_widget)
        self.fields_layout.setContentsMargins(0, 0, 0, 0)
        self.fields_layout.setSpacing(4)
        self.fields_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.fields_scroll.setWidget(self.fields_widget)

        left_layout.addWidget(fields_label)
        left_layout.addWidget(self.fields_scroll, 1)

        # ===== ЦЕНТРАЛЬНАЯ ПАНЕЛЬ =====
        center_panel = QWidget()
        center_panel.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
            }
        """)

        center_layout = QVBoxLayout(center_panel)
        center_layout.setContentsMargins(8, 8, 8, 8)
        center_layout.setSpacing(8)

        # Панель операторов
        operators_label = QLabel("🔧 ОПЕРАТОРЫ")
        operators_label.setStyleSheet("color: #4ec9b0; font-weight: bold;")

        operators_widget = QWidget()
        operators_layout = QGridLayout(operators_widget)
        operators_layout.setSpacing(4)

        operators = [
            ("+", "Сложение", 0, 0),
            ("-", "Вычитание", 0, 1),
            ("*", "Умножение", 0, 2),
            ("/", "Деление", 0, 3),
            ("=", "Равно", 1, 0),
            ("<>", "Не равно", 1, 1),
            (">", "Больше", 1, 2),
            ("<", "Меньше", 1, 3),
            (">=", "Больше или равно", 2, 0),
            ("<=", "Меньше или равно", 2, 1),
            ("&", "Объединение строк", 2, 2),
        ]

        for op, tip, row, col in operators:
            btn = OperatorButton(op, tip)
            btn.clicked.connect(lambda checked, o=op: self.add_to_formula(f" {o} "))
            operators_layout.addWidget(btn, row, col)

        # Панель функций
        functions_label = QLabel("📊 ФУНКЦИИ")
        functions_label.setStyleSheet("color: #4ec9b0; font-weight: bold; margin-top: 8px;")

        functions_widget = QWidget()
        functions_layout = QGridLayout(functions_widget)
        functions_layout.setSpacing(4)

        functions = [
            ("SUM", "Сумма", 0, 0),
            ("AVG", "Среднее", 0, 1),
            ("COUNT", "Количество", 0, 2),
            ("MIN", "Минимум", 0, 3),
            ("MAX", "Максимум", 1, 0),
            ("ROUND", "Округление", 1, 1),
            ("ABS", "Модуль числа", 1, 2),
            ("YEAR", "Год из даты", 1, 3),
            ("MONTH", "Месяц из даты", 2, 0),
            ("DAY", "День из даты", 2, 1),
            ("NOW", "Текущая дата", 2, 2),
        ]

        for func, tip, row, col in functions:
            btn = FunctionButton(func, tip)
            btn.clicked.connect(lambda checked, f=func: self.add_to_formula(f"{f}()"))
            functions_layout.addWidget(btn, row, col)

        # Панель условий
        conditions_label = QLabel("⚖️ УСЛОВИЯ")
        conditions_label.setStyleSheet("color: #4ec9b0; font-weight: bold; margin-top: 8px;")

        conditions_widget = QWidget()
        conditions_layout = QHBoxLayout(conditions_widget)
        conditions_layout.setSpacing(4)

        if_btn = ConditionButton("ЕСЛИ", "Условный оператор")
        if_btn.clicked.connect(lambda: self.add_to_formula("ЕСЛИ(условие; значение_если_истина; значение_если_ложь)"))

        and_btn = ConditionButton("И", "Логическое И")
        and_btn.clicked.connect(lambda: self.add_to_formula(" И "))

        or_btn = ConditionButton("ИЛИ", "Логическое ИЛИ")
        or_btn.clicked.connect(lambda: self.add_to_formula(" ИЛИ "))

        not_btn = ConditionButton("НЕ", "Логическое НЕ")
        not_btn.clicked.connect(lambda: self.add_to_formula("НЕ()"))

        conditions_layout.addWidget(if_btn)
        conditions_layout.addWidget(and_btn)
        conditions_layout.addWidget(or_btn)
        conditions_layout.addWidget(not_btn)

        # Работа со строками
        strings_label = QLabel("📝 РАБОТА СО СТРОКАМИ")
        strings_label.setStyleSheet("color: #4ec9b0; font-weight: bold; margin-top: 8px;")

        strings_widget = QWidget()
        strings_layout = QGridLayout(strings_widget)
        strings_layout.setSpacing(4)

        string_funcs = [
            ("UPPER", "ВСЕ ПРОПИСНЫЕ", 0, 0),
            ("LOWER", "все строчные", 0, 1),
            ("PROPER", "Первая Прописная", 0, 2),
            ("LEFT", "Левые символы", 1, 0),
            ("RIGHT", "Правые символы", 1, 1),
            ("MID", "Середина текста", 1, 2),
            ("LEN", "Длина текста", 2, 0),
            ("TRIM", "Удалить пробелы", 2, 1),
        ]

        for func, tip, row, col in string_funcs:
            btn = FunctionButton(func, tip)
            btn.clicked.connect(lambda checked, f=func: self.add_to_formula(f"{f}()"))
            strings_layout.addWidget(btn, row, col)

        # Сборка центральной панели
        center_layout.addWidget(operators_label)
        center_layout.addWidget(operators_widget)
        center_layout.addWidget(functions_label)
        center_layout.addWidget(functions_widget)
        center_layout.addWidget(conditions_label)
        center_layout.addWidget(conditions_widget)
        center_layout.addWidget(strings_label)
        center_layout.addWidget(strings_widget)
        center_layout.addStretch()

        # ===== ПРАВАЯ ПАНЕЛЬ =====
        right_panel = QWidget()
        right_panel.setStyleSheet("""
            QWidget {
                background-color: #252526;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
            }
        """)

        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(8, 8, 8, 8)
        right_layout.setSpacing(8)

        # Редактор формулы
        formula_label = QLabel("🧮 ФОРМУЛА")
        formula_label.setStyleSheet("color: #4ec9b0; font-weight: bold;")

        self.formula_edit = QTextEdit()
        self.formula_edit.setPlainText(self.formula)
        self.formula_edit.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ce9178;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                font-family: monospace;
                font-size: 14px;
                padding: 8px;
            }
        """)
        self.formula_edit.setMinimumHeight(150)

        # Кнопки очистки
        clear_btn = QPushButton("🗑️ Очистить")
        clear_btn.clicked.connect(self.clear_formula)

        # Предпросмотр результата
        preview_label = QLabel("👁️ ПРЕДПРОСМОТР")
        preview_label.setStyleSheet("color: #4ec9b0; font-weight: bold; margin-top: 8px;")

        self.preview_text = QLabel("Результат будет показан здесь")
        self.preview_text.setStyleSheet("""
            QLabel {
                background-color: #1e1e1e;
                color: #9cdcfe;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                padding: 8px;
                min-height: 60px;
            }
        """)
        self.preview_text.setWordWrap(True)

        # Кнопки диалога
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        # Сборка правой панели
        right_layout.addWidget(formula_label)
        right_layout.addWidget(self.formula_edit)
        right_layout.addWidget(clear_btn)
        right_layout.addWidget(preview_label)
        right_layout.addWidget(self.preview_text, 1)
        right_layout.addWidget(button_box)

        # Сборка главного окна
        main_layout.addWidget(left_panel)
        main_layout.addWidget(center_panel, 1)
        main_layout.addWidget(right_panel, 1)

    def load_fields(self):
        """Загружает поля текущей таблицы"""
        # TODO: получать поля из project_manager
        # Пока заглушка
        test_fields = [
            {"name": "Имя", "type": "TEXT"},
            {"name": "Фамилия", "type": "TEXT"},
            {"name": "Возраст", "type": "INTEGER"},
            {"name": "Дата рождения", "type": "DATE"},
            {"name": "Сумма", "type": "MONEY"},
        ]

        for field in test_fields:
            btn = FieldButton(field["name"], field)
            btn.clicked.connect(lambda checked, f=field: self.add_to_formula(f"[{f['name']}]"))
            self.fields_layout.addWidget(btn)

    def add_to_formula(self, text):
        """Добавляет текст в формулу"""
        cursor = self.formula_edit.textCursor()
        cursor.insertText(text)
        self.formula_edit.setTextCursor(cursor)
        self.formula_edit.setFocus()
        self.update_preview()

    def clear_formula(self):
        """Очищает формулу"""
        self.formula_edit.clear()
        self.update_preview()

    def update_preview(self):
        """Обновляет предпросмотр результата"""
        formula = self.formula_edit.toPlainText()
        if not formula:
            self.preview_text.setText("Введите формулу")
            return

        # TODO: реальный парсинг и вычисление
        # Пока просто показываем формулу
        self.preview_text.setText(f"Результат вычисления:\n{formula}")

    def get_formula(self):
        """Возвращает введённую формулу"""
        return self.formula_edit.toPlainText()