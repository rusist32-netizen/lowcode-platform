# -*- coding: utf-8 -*-

"""
Плитка типа поля для перетаскивания
"""

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class FieldTile(QFrame):
    """Плитка типа поля для перетаскивания"""
    
    # Сигналы для отслеживания состояния
    dragStarted = pyqtSignal()      # Нажали на плитку
    dragFinished = pyqtSignal()      # Отпустили плитку
    
    def __init__(self, icon: str, title: str, description: str, type_id: str, parent=None):
        super().__init__(parent)
        
        self.type_id = type_id
        self.title = title
        self.icon = icon
        
        # Размер плитки
        self.setFixedSize(90, 90)
        self.setCursor(Qt.CursorShape.OpenHandCursor)
        self.setFrameStyle(QFrame.Shape.Box)
        
        # Стиль плитки
        self.setStyleSheet("""
            FieldTile {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 6px;
            }
            FieldTile:hover {
                background-color: #2d3a4f;
                border: 2px solid #3b82f6;
            }
        """)
        
        # Создаем layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(2)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Иконка типа поля
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 28px; background: transparent;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)
        
        # Название типа поля
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #e2e8f0; font-weight: 500; font-size: 10px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setWordWrap(True)
        layout.addWidget(title_label)
        
        # Всплывающая подсказка
        self.setToolTip(description)
        
        # Для отслеживания начала перетаскивания
        self.drag_start_position = None
        self.pressed = False
    
    def mousePressEvent(self, event):
        """Нажатие на плитку"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.pressed = True
            self.drag_start_position = event.pos()
            print(f"🖱️ Нажата плитка: {self.title}")
            # Сигнал о начале
            self.dragStarted.emit()
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        """Начало перетаскивания"""
        if self.pressed and event.buttons() == Qt.MouseButton.LeftButton:
            # Проверяем, достаточно ли сдвинули мышь для начала перетаскивания
            if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
                return
            
            print(f"🚀 Перетаскивание: {self.title}")
            
            # Создаем объект перетаскивания
            drag = QDrag(self)
            mime = QMimeData()
            
            # Передаем только type_id
            data = f"{self.type_id}"
            mime.setText(data)
            drag.setMimeData(mime)
            
            # Создаем изображение для перетаскивания
            pixmap = self.grab()
            drag.setPixmap(pixmap)
            drag.setHotSpot(event.pos())
            
            # Запускаем перетаскивание
            result = drag.exec(Qt.DropAction.CopyAction)
            
            self.pressed = False
            print(f"✅ Перетаскивание завершено: {self.title}")
            self.dragFinished.emit()
    
    def mouseReleaseEvent(self, event):
        """Отпускание кнопки мыши"""
        if self.pressed and event.button() == Qt.MouseButton.LeftButton:
            self.pressed = False
            print(f"🖱️ Отпущена плитка (без перетаскивания): {self.title}")
            self.dragFinished.emit()
        super().mouseReleaseEvent(event)