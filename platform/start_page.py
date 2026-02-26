#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Стартовая страница приложения
"""

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class StartPage(QWidget):
    """
    Стартовая страница с кнопками создания/открытия проекта
    """

    newProjectRequested = pyqtSignal()
    openProjectRequested = pyqtSignal()

    def __init__(self, project_manager=None, parent=None):
        super().__init__(parent)
        self.project_manager = project_manager
        self.setup_ui()

    def setup_ui(self):
        """Создание интерфейса стартовой страницы"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(30)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Заголовок
        title = QLabel("🚀 Low-Code Платформа")
        title.setStyleSheet("""
            QLabel {
                color: #4ec9b0;
                font-size: 36px;
                font-weight: bold;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Подзаголовок
        subtitle = QLabel("Создавайте приложения без написания кода")
        subtitle.setStyleSheet("""
            QLabel {
                color: #888;
                font-size: 16px;
            }
        """)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)

        # Контейнер для кнопок
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setSpacing(20)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Кнопка нового проекта
        new_btn = QPushButton("➕ Новый проект")
        new_btn.setFixedSize(200, 60)
        new_btn.setStyleSheet("""
            QPushButton {
                background-color: #0e639c;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1177bb;
            }
        """)
        new_btn.clicked.connect(self.newProjectRequested.emit)

        # Кнопка открытия проекта
        open_btn = QPushButton("📂 Открыть проект")
        open_btn.setFixedSize(200, 60)
        open_btn.setStyleSheet("""
            QPushButton {
                background-color: #4c4c4c;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5c5c5c;
            }
        """)
        open_btn.clicked.connect(self.openProjectRequested.emit)

        button_layout.addWidget(new_btn)
        button_layout.addWidget(open_btn)

        layout.addWidget(button_container)

        # Информация о последних проектах (если есть)
        if self.project_manager and self.project_manager.get_recent_projects():
            recent_label = QLabel("Недавние проекты:")
            recent_label.setStyleSheet("color: #888; font-size: 12px; margin-top: 30px;")
            layout.addWidget(recent_label)

            recent_widget = QWidget()
            recent_layout = QVBoxLayout(recent_widget)
            recent_layout.setSpacing(5)

            for project in self.project_manager.get_recent_projects():
                btn = QPushButton(f"📁 {project['name']}")
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #2d2d2d;
                        color: #e0e0e0;
                        border: 1px solid #4c4c4c;
                        border-radius: 4px;
                        padding: 8px;
                        text-align: left;
                    }
                    QPushButton:hover {
                        background-color: #3c3c3c;
                    }
                """)
                btn.clicked.connect(lambda checked, p=project: self.open_recent_project(p))
                recent_layout.addWidget(btn)

            layout.addWidget(recent_widget)

    def open_recent_project(self, project):
        """Открывает недавний проект"""
        # TODO: реализовать открытие проекта по пути
        pass