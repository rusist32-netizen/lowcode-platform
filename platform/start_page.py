# -*- coding: utf-8 -*-

"""
Стартовая страница
"""

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class StartPage(QWidget):
    """Стартовая страница"""
    
    newProject = pyqtSignal()
    openProject = pyqtSignal(str)
    
    def __init__(self, project_manager, parent=None):
        super().__init__(parent)
        
        self.project_manager = project_manager
        
        self._setup_ui()
        self._load_recent_projects()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(30)
        
        # Логотип
        logo = QLabel("🚀")
        logo.setStyleSheet("font-size: 120px; color: #3b82f6;")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo)
        
        # Заголовок
        title = QLabel("No-Code Platform")
        title.setStyleSheet("font-size: 48px; font-weight: bold; color: #3b82f6;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Подзаголовок
        subtitle = QLabel("Создавайте приложения без единой строки кода")
        subtitle.setStyleSheet("font-size: 18px; color: #94a3b8;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        # Кнопки
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)
        
        new_btn = QPushButton("📁 Новый проект")
        new_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        new_btn.setFixedSize(200, 50)
        new_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        new_btn.clicked.connect(self.newProject.emit)
        btn_layout.addWidget(new_btn)
        
        open_btn = QPushButton("📂 Открыть проект")
        open_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        open_btn.setFixedSize(200, 50)
        open_btn.setStyleSheet("""
            QPushButton {
                background-color: #1e293b;
                color: #e2e8f0;
                border: 2px solid #334155;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2d3a4f;
                border-color: #3b82f6;
            }
        """)
        open_btn.clicked.connect(lambda: self.openProject.emit(""))
        btn_layout.addWidget(open_btn)
        
        layout.addLayout(btn_layout)
        
        # Последние проекты
        recent_label = QLabel("Последние проекты")
        recent_label.setStyleSheet("color: #e2e8f0; font-size: 14px; margin-top: 40px;")
        recent_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(recent_label)
        
        self.recent_list = QListWidget()
        self.recent_list.setMaximumWidth(600)
        self.recent_list.setMinimumHeight(200)
        self.recent_list.setStyleSheet("""
            QListWidget {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 8px;
                color: #e2e8f0;
                padding: 10px;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 10px;
                border-radius: 4px;
                margin: 2px 0;
            }
            QListWidget::item:hover {
                background-color: #2d3a4f;
            }
            QListWidget::item:selected {
                background-color: #3b82f6;
            }
        """)
        self.recent_list.itemDoubleClicked.connect(self._open_recent)
        layout.addWidget(self.recent_list)
    
    def _load_recent_projects(self):
        self.recent_list.clear()
        
        projects = self.project_manager.list_projects()
        for proj in projects[:10]:
            item = QListWidgetItem(f"{proj['name']} — {proj['modified'][:10]}")
            item.setData(Qt.ItemDataRole.UserRole, proj['path'])
            self.recent_list.addItem(item)
    
    def _open_recent(self, item):
        path = item.data(Qt.ItemDataRole.UserRole)
        self.openProject.emit(path)