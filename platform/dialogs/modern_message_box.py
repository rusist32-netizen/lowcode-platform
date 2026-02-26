#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Современное окно сообщений
"""

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class ModernMessageBox(QDialog):
    """
    Современное окно сообщений с красивым дизайном
    """

    @staticmethod
    def info(parent, title, message):
        """Информационное сообщение"""
        dialog = ModernMessageBox(parent, title, message, "info")
        return dialog.exec()

    @staticmethod
    def success(parent, title, message):
        """Сообщение об успехе"""
        dialog = ModernMessageBox(parent, title, message, "success")
        return dialog.exec()

    @staticmethod
    def warning(parent, title, message):
        """Предупреждение"""
        dialog = ModernMessageBox(parent, title, message, "warning")
        return dialog.exec()

    @staticmethod
    def error(parent, title, message):
        """Сообщение об ошибке"""
        dialog = ModernMessageBox(parent, title, message, "error")
        return dialog.exec()

    @staticmethod
    def question(parent, title, message):
        """Вопрос с кнопками Да/Нет"""
        dialog = ModernMessageBox(parent, title, message, "question")
        return dialog.exec() == QDialog.DialogCode.Accepted

    def __init__(self, parent, title, message, msg_type="info"):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setModal(True)
        self.setFixedSize(400, 200)

        self.setup_ui(title, message, msg_type)
        self.center_on_parent()

    def setup_ui(self, title, message, msg_type):
        """Создание интерфейса"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Контейнер
        container = QWidget()
        container.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
                border: 1px solid #3c3c3c;
                border-radius: 8px;
            }
        """)

        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(20, 20, 20, 20)
        container_layout.setSpacing(15)

        # Заголовок с иконкой
        title_layout = QHBoxLayout()

        # Иконка в зависимости от типа
        icon_label = QLabel()
        icon_label.setFixedSize(24, 24)
        icon_label.setStyleSheet("font-size: 20px;")

        if msg_type == "info":
            icon_label.setText("ℹ️")
            title_color = "#4ec9b0"
        elif msg_type == "success":
            icon_label.setText("✅")
            title_color = "#4ec9b0"
        elif msg_type == "warning":
            icon_label.setText("⚠️")
            title_color = "#f4a261"
        elif msg_type == "error":
            icon_label.setText("❌")
            title_color = "#f14c4c"
        elif msg_type == "question":
            icon_label.setText("❓")
            title_color = "#4ec9b0"

        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {title_color}; font-weight: bold; font-size: 14px;")

        title_layout.addWidget(icon_label)
        title_layout.addWidget(title_label)
        title_layout.addStretch()

        container_layout.addLayout(title_layout)

        # Сообщение
        msg_label = QLabel(message)
        msg_label.setWordWrap(True)
        msg_label.setStyleSheet("color: #e0e0e0; font-size: 12px; min-height: 60px;")
        container_layout.addWidget(msg_label)

        # Кнопки
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        if msg_type == "question":
            # Кнопки Да/Нет
            no_btn = QPushButton("Нет")
            no_btn.setFixedSize(80, 30)
            no_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4c4c4c;
                    color: white;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #5c5c5c;
                }
            """)
            no_btn.clicked.connect(self.reject)

            yes_btn = QPushButton("Да")
            yes_btn.setFixedSize(80, 30)
            yes_btn.setStyleSheet("""
                QPushButton {
                    background-color: #0e639c;
                    color: white;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #1177bb;
                }
            """)
            yes_btn.clicked.connect(self.accept)

            button_layout.addWidget(no_btn)
            button_layout.addWidget(yes_btn)
        else:
            # Одна кнопка ОК
            ok_btn = QPushButton("OK")
            ok_btn.setFixedSize(80, 30)
            ok_btn.setStyleSheet("""
                QPushButton {
                    background-color: #0e639c;
                    color: white;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #1177bb;
                }
            """)
            ok_btn.clicked.connect(self.accept)
            button_layout.addWidget(ok_btn)

        container_layout.addLayout(button_layout)

        layout.addWidget(container)

    def center_on_parent(self):
        """Центрирует окно относительно родителя"""
        if self.parent():
            parent_geo = self.parent().geometry()
            x = parent_geo.x() + (parent_geo.width() - self.width()) // 2
            y = parent_geo.y() + (parent_geo.height() - self.height()) // 2
            self.move(x, y)
        else:
            # Центрируем по экрану
            screen = QApplication.primaryScreen().geometry()
            self.move(screen.center() - self.rect().center())