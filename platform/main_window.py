# -*- coding: utf-8 -*-

"""
Главное окно с ленточным меню
"""

import sys
import os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from platform.project_manager import ProjectManager
from platform.start_page import StartPage
from platform.designers.table_designer import TableDesignerWidget  # ← ИСПРАВЛЕНО!


class RibbonButton(QToolButton):
    """Кнопка в ленточном меню"""
    
    def __init__(self, text: str, icon_text: str = "", parent=None):
        super().__init__(parent)
        
        self.setText(text)
        if icon_text:
            self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
            self.setIcon(self._create_icon(icon_text))
        
        self.setFixedSize(70, 60)
        self.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.setStyleSheet("""
            QToolButton {
                background-color: transparent;
                color: #e2e8f0;
                border: none;
                border-radius: 4px;
                font-size: 11px;
                padding: 5px;
            }
            QToolButton:hover {
                background-color: #3b82f6;
            }
            QToolButton:pressed {
                background-color: #2563eb;
            }
            QToolButton::menu-indicator {
                image: none;
            }
        """)
    
    def _create_icon(self, text: str) -> QIcon:
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setPen(QColor("#e2e8f0"))
        painter.setFont(QFont("Segoe UI", 16))
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, text)
        painter.end()
        
        return QIcon(pixmap)


class RibbonBar(QWidget):
    """Ленточное меню"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setFixedHeight(120)
        self.setStyleSheet("""
            QWidget {
                background-color: #1e293b;
                border-bottom: 2px solid #3b82f6;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.tabs_bar = QTabBar()
        self.tabs_bar.setExpanding(False)
        self.tabs_bar.setDrawBase(False)
        self.tabs_bar.setStyleSheet("""
            QTabBar::tab {
                background-color: transparent;
                color: #94a3b8;
                padding: 8px 20px;
                margin-top: 5px;
                font-size: 12px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }
            QTabBar::tab:hover {
                background-color: #2d3a4f;
                color: #e2e8f0;
            }
            QTabBar::tab:selected {
                background-color: #3b82f6;
                color: white;
            }
        """)
        
        tabs = ["Файл", "Конструктор", "Формы", "Отчеты", "Логика", "Сервис", "Вид", "?"]
        for tab in tabs:
            self.tabs_bar.addTab(tab)
        
        self.tabs_bar.setCurrentIndex(1)
        
        layout.addWidget(self.tabs_bar)
        
        self.stack = QStackedWidget()
        layout.addWidget(self.stack)
        
        self._create_file_tab()
        self._create_designer_tab()
        self._create_forms_tab()
        self._create_reports_tab()
        self._create_logic_tab()
        self._create_service_tab()
        self._create_view_tab()
        self._create_help_tab()
        
        self.tabs_bar.currentChanged.connect(self.stack.setCurrentIndex)
    
    def _create_button_group(self, title: str) -> QGroupBox:
        group = QGroupBox(title)
        group.setStyleSheet("""
            QGroupBox {
                color: #94a3b8;
                border: 1px solid #334155;
                border-radius: 4px;
                margin-top: 10px;
                font-size: 11px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        layout = QHBoxLayout(group)
        layout.setContentsMargins(5, 15, 5, 5)
        layout.setSpacing(5)
        
        return group
    
    def _create_file_tab(self):
        tab = QWidget()
        layout = QHBoxLayout(tab)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(20)
        
        project_group = self._create_button_group("Проект")
        project_group.layout().addWidget(RibbonButton("Новый", "📁"))
        project_group.layout().addWidget(RibbonButton("Открыть", "📂"))
        project_group.layout().addWidget(RibbonButton("Сохранить", "💾"))
        layout.addWidget(project_group)
        
        export_group = self._create_button_group("Экспорт")
        export_group.layout().addWidget(RibbonButton("Excel", "📊"))
        export_group.layout().addWidget(RibbonButton("PDF", "📄"))
        export_group.layout().addWidget(RibbonButton("JSON", "🔧"))
        layout.addWidget(export_group)
        
        exit_group = self._create_button_group("Выход")
        exit_group.layout().addWidget(RibbonButton("Закрыть", "❌"))
        layout.addWidget(exit_group)
        
        layout.addStretch()
        self.stack.addWidget(tab)
    
    def _create_designer_tab(self):
        tab = QWidget()
        layout = QHBoxLayout(tab)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(20)
        
        tables_group = self._create_button_group("Таблицы")
        tables_group.layout().addWidget(RibbonButton("Создать", "➕"))
        tables_group.layout().addWidget(RibbonButton("Открыть", "📂"))
        tables_group.layout().addWidget(RibbonButton("Удалить", "🗑️"))
        layout.addWidget(tables_group)
        
        fields_group = self._create_button_group("Поля")
        fields_group.layout().addWidget(RibbonButton("Добавить", "➕"))
        fields_group.layout().addWidget(RibbonButton("Изменить", "✏️"))
        fields_group.layout().addWidget(RibbonButton("Удалить", "❌"))
        layout.addWidget(fields_group)
        
        formats_group = self._create_button_group("Форматы")
        formats_group.layout().addWidget(RibbonButton("Текст", "📝"))
        formats_group.layout().addWidget(RibbonButton("Число", "🔢"))
        formats_group.layout().addWidget(RibbonButton("Дата", "📅"))
        layout.addWidget(formats_group)
        
        view_group = self._create_button_group("Вид")
        view_group.layout().addWidget(RibbonButton("Обновить", "🔄"))
        view_group.layout().addWidget(RibbonButton("Свойства", "⚙️"))
        layout.addWidget(view_group)
        
        layout.addStretch()
        self.stack.addWidget(tab)
    
    def _create_forms_tab(self):
        tab = QWidget()
        layout = QHBoxLayout(tab)
        layout.addWidget(QLabel("Конструктор форм (будет позже)"))
        layout.addStretch()
        self.stack.addWidget(tab)
    
    def _create_reports_tab(self):
        tab = QWidget()
        layout = QHBoxLayout(tab)
        layout.addWidget(QLabel("Конструктор отчетов (будет позже)"))
        layout.addStretch()
        self.stack.addWidget(tab)
    
    def _create_logic_tab(self):
        tab = QWidget()
        layout = QHBoxLayout(tab)
        layout.addWidget(QLabel("Конструктор логики (будет позже)"))
        layout.addStretch()
        self.stack.addWidget(tab)
    
    def _create_service_tab(self):
        tab = QWidget()
        layout = QHBoxLayout(tab)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(20)
        
        settings_group = self._create_button_group("Настройки")
        settings_group.layout().addWidget(RibbonButton("Темы", "🎨"))
        settings_group.layout().addWidget(RibbonButton("Язык", "🌐"))
        layout.addWidget(settings_group)
        
        tools_group = self._create_button_group("Инструменты")
        tools_group.layout().addWidget(RibbonButton("Проверка", "✓"))
        tools_group.layout().addWidget(RibbonButton("Оптимизация", "⚡"))
        layout.addWidget(tools_group)
        
        layout.addStretch()
        self.stack.addWidget(tab)
    
    def _create_view_tab(self):
        tab = QWidget()
        layout = QHBoxLayout(tab)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(20)
        
        panels_group = self._create_button_group("Панели")
        panels_group.layout().addWidget(RibbonButton("Таблицы", "📋"))
        panels_group.layout().addWidget(RibbonButton("Типы полей", "🔧"))
        panels_group.layout().addWidget(RibbonButton("Свойства", "⚙️"))
        layout.addWidget(panels_group)
        
        layout.addStretch()
        self.stack.addWidget(tab)
    
    def _create_help_tab(self):
        tab = QWidget()
        layout = QHBoxLayout(tab)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(20)
        
        help_group = self._create_button_group("Справка")
        help_group.layout().addWidget(RibbonButton("Справка", "❓"))
        help_group.layout().addWidget(RibbonButton("О программе", "ℹ️"))
        layout.addWidget(help_group)
        
        layout.addStretch()
        self.stack.addWidget(tab)


class MainWindow(QMainWindow):
    """Главное окно"""
    
    def __init__(self):
        super().__init__()
        
        self.project_manager = ProjectManager()
        
        self.setWindowTitle("No-Code Platform")
        self.setGeometry(100, 100, 1400, 900)
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0f172a;
            }
            QStatusBar {
                background-color: #1e293b;
                color: #94a3b8;
                border-top: 1px solid #334155;
            }
        """)
        
        self._setup_ui()
        self._show_start_page()
    
    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.ribbon = RibbonBar()
        layout.addWidget(self.ribbon)
        
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self._close_tab)
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                background-color: #0f172a;
                border: none;
            }
            QTabBar::tab {
                background-color: #1e293b;
                color: #94a3b8;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }
            QTabBar::tab:hover {
                background-color: #2d3a4f;
                color: #e2e8f0;
            }
            QTabBar::tab:selected {
                background-color: #3b82f6;
                color: white;
            }
        """)
        layout.addWidget(self.tab_widget)
        
        self.status_label = QLabel("Готов к работе")
        self.statusBar().addWidget(self.status_label)
    
    def _show_start_page(self):
        start_page = StartPage(self.project_manager, self)
        start_page.openProject.connect(self._open_project)
        start_page.newProject.connect(self._new_project)
        
        index = self.tab_widget.addTab(start_page, "🏠 Стартовая")
        self.tab_widget.setCurrentIndex(index)
    
    def _new_project(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Новый проект")
        dialog.setModal(True)
        dialog.setFixedSize(500, 300)
        
        layout = QVBoxLayout(dialog)
        
        layout.addWidget(QLabel("Название проекта:"))
        name_edit = QLineEdit()
        name_edit.setPlaceholderText("например: Смарт Завуч")
        layout.addWidget(name_edit)
        
        layout.addWidget(QLabel("Описание (необязательно):"))
        desc_edit = QTextEdit()
        desc_edit.setMaximumHeight(100)
        layout.addWidget(desc_edit)
        
        layout.addWidget(QLabel("Автор:"))
        author_edit = QLineEdit()
        layout.addWidget(author_edit)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        cancel_btn = QPushButton("Отмена")
        cancel_btn.clicked.connect(dialog.reject)
        btn_layout.addWidget(cancel_btn)
        
        ok_btn = QPushButton("Создать")
        ok_btn.setStyleSheet("background-color: #3b82f6; color: white;")
        ok_btn.clicked.connect(dialog.accept)
        btn_layout.addWidget(ok_btn)
        
        layout.addLayout(btn_layout)
        
        if dialog.exec() == QDialog.DialogCode.Accepted and name_edit.text():
            project = self.project_manager.create_project(
                name=name_edit.text(),
                description=desc_edit.toPlainText(),
                author=author_edit.text()
            )
            
            self.status_label.setText(f"Проект '{project.name}' создан")
            
            self.tab_widget.removeTab(0)
            self._open_table_designer()
    
    def _open_project(self, filename: str = None):
        if not filename:
            filename, _ = QFileDialog.getOpenFileName(
                self, "Открыть проект", "projects", "No-Code Project (*.ncp)"
            )
        
        if filename:
            project = self.project_manager.load_project(filename)
            if project:
                self.status_label.setText(f"Проект '{project.name}' загружен")
                self.tab_widget.removeTab(0)
                self._open_table_designer()
    
    def _open_table_designer(self):
        if not self.project_manager.current_project:
            QMessageBox.warning(self, "Внимание", "Сначала создайте или откройте проект")
            return
        
        for i in range(self.tab_widget.count()):
            if self.tab_widget.tabText(i) == "📊 Конструктор таблиц":
                self.tab_widget.setCurrentIndex(i)
                return
        
        designer = TableDesignerWidget(self.project_manager)
        index = self.tab_widget.addTab(designer, "📊 Конструктор таблиц")
        self.tab_widget.setCurrentIndex(index)
    
    def _close_tab(self, index: int):
        widget = self.tab_widget.widget(index)
        if hasattr(widget, 'can_close') and not widget.can_close():
            return
        self.tab_widget.removeTab(index)
        widget.deleteLater()