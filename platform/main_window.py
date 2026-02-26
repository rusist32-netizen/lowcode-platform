#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Главное окно приложения
"""

import os
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from platform.project_manager import ProjectManager
from platform.start_page import StartPage
from platform.designers.table_designer import TableDesigner
from platform.dialogs.modern_message_box import ModernMessageBox


class MainWindow(QMainWindow):
    """
    Главное окно платформы
    """

    def __init__(self):
        super().__init__()
        self.project_manager = None
        self.current_project_path = None
        self.current_designer = None

        self.setWindowTitle("Low-Code Платформа")
        self.setGeometry(100, 100, 1400, 800)

        self.setup_ui()
        self.setup_menu()
        self.setup_status_bar()

        # Показываем стартовую страницу
        self.show_start_page()

    def setup_ui(self):
        """Создание основного интерфейса"""
        # Центральный виджет с вкладками
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                background-color: #1e1e1e;
                border: none;
            }
            QTabBar::tab {
                background-color: #2d2d2d;
                color: #e0e0e0;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:hover {
                background-color: #3c3c3c;
            }
            QTabBar::tab:selected {
                background-color: #0e639c;
                color: white;
            }
        """)

        self.setCentralWidget(self.tab_widget)

    def setup_menu(self):
        """Создание меню приложения"""
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border-bottom: 1px solid #3c3c3c;
            }
            QMenuBar::item {
                padding: 6px 10px;
            }
            QMenuBar::item:selected {
                background-color: #3c3c3c;
            }
            QMenu {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #3c3c3c;
            }
            QMenu::item:selected {
                background-color: #0e639c;
            }
        """)

        # Меню Файл
        file_menu = menubar.addMenu("Файл")

        new_project_action = QAction("Новый проект", self)
        new_project_action.triggered.connect(self.new_project)
        file_menu.addAction(new_project_action)

        open_project_action = QAction("Открыть проект", self)
        open_project_action.triggered.connect(self.open_project)
        file_menu.addAction(open_project_action)

        file_menu.addSeparator()

        save_project_action = QAction("Сохранить проект", self)
        save_project_action.triggered.connect(self.save_project)
        file_menu.addAction(save_project_action)

        save_project_as_action = QAction("Сохранить проект как...", self)
        save_project_as_action.triggered.connect(self.save_project_as)
        file_menu.addAction(save_project_as_action)

        file_menu.addSeparator()

        close_project_action = QAction("Закрыть проект", self)
        close_project_action.triggered.connect(self.close_project)
        file_menu.addAction(close_project_action)

        file_menu.addSeparator()

        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Меню Конструкторы
        designers_menu = menubar.addMenu("Конструкторы")

        table_designer_action = QAction("Конструктор таблиц", self)
        table_designer_action.triggered.connect(self.open_table_designer)
        designers_menu.addAction(table_designer_action)

        form_designer_action = QAction("Конструктор форм", self)
        form_designer_action.triggered.connect(self.open_form_designer)
        designers_menu.addAction(form_designer_action)

        report_designer_action = QAction("Конструктор отчётов", self)
        report_designer_action.triggered.connect(self.open_report_designer)
        designers_menu.addAction(report_designer_action)

        menu_designer_action = QAction("Конструктор меню", self)
        menu_designer_action.triggered.connect(self.open_menu_designer)
        designers_menu.addAction(menu_designer_action)

        logic_designer_action = QAction("Конструктор логики", self)
        logic_designer_action.triggered.connect(self.open_logic_designer)
        designers_menu.addAction(logic_designer_action)

        # Меню Справка
        help_menu = menubar.addMenu("Справка")

        about_action = QAction("О программе", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def setup_status_bar(self):
        """Создание строки статуса"""
        self.statusBar().setStyleSheet("""
            QStatusBar {
                background-color: #1e1e1e;
                color: #888;
                border-top: 1px solid #3c3c3c;
            }
        """)
        self.status_label = QLabel("Готов к работе")
        self.statusBar().addWidget(self.status_label)

    def show_start_page(self):
        """Показывает стартовую страницу"""
        self.start_page = StartPage(self.project_manager)
        self.start_page.newProjectRequested.connect(self.new_project)
        self.start_page.openProjectRequested.connect(self.open_project)
        self.setCentralWidget(self.start_page)

    # ========== РАБОТА С ПРОЕКТАМИ ==========

    def new_project(self):
        """Создание нового проекта"""
        # Запрашиваем название проекта
        project_name, ok = QInputDialog.getText(
            self, "Новый проект",
            "Введите название проекта:"
        )

        if not ok or not project_name.strip():
            return

        # Запрашиваем папку для сохранения
        projects_dir = os.path.join(os.path.expanduser("~"), "LowCodeProjects")
        if not os.path.exists(projects_dir):
            os.makedirs(projects_dir)

        project_path = os.path.join(projects_dir, project_name.strip())

        try:
            # Создаём проект
            self.project_manager = ProjectManager(project_path)
            self.project_manager.create_project(project_name.strip())

            self.current_project_path = project_path
            self.status_label.setText(f"Проект: {project_name}")

            # Открываем конструктор таблиц
            self.open_table_designer()

        except Exception as e:
            ModernMessageBox.error(self, "Ошибка", f"Не удалось создать проект: {str(e)}")

    def open_project(self):
        """Открытие существующего проекта"""
        projects_dir = os.path.join(os.path.expanduser("~"), "LowCodeProjects")

        if not os.path.exists(projects_dir):
            os.makedirs(projects_dir)

        project_path = QFileDialog.getExistingDirectory(
            self, "Выберите папку проекта", projects_dir
        )

        if not project_path:
            return

        try:
            # Открываем проект
            self.project_manager = ProjectManager(project_path)
            self.project_manager.load_project()

            self.current_project_path = project_path
            project_name = os.path.basename(project_path)
            self.status_label.setText(f"Проект: {project_name}")

            # Открываем конструктор таблиц
            self.open_table_designer()

        except Exception as e:
            ModernMessageBox.error(self, "Ошибка", f"Не удалось открыть проект: {str(e)}")

    def save_project(self):
        """Сохранение проекта"""
        if not self.project_manager:
            ModernMessageBox.warning(self, "Предупреждение", "Нет открытого проекта")
            return

        try:
            self.project_manager.save_project()
            self.status_label.setText("Проект сохранён")
        except Exception as e:
            ModernMessageBox.error(self, "Ошибка", f"Не удалось сохранить проект: {str(e)}")

    def save_project_as(self):
        """Сохранение проекта как..."""
        if not self.project_manager:
            ModernMessageBox.warning(self, "Предупреждение", "Нет открытого проекта")
            return

        projects_dir = os.path.join(os.path.expanduser("~"), "LowCodeProjects")
        new_path = QFileDialog.getExistingDirectory(
            self, "Выберите папку для сохранения", projects_dir
        )

        if not new_path:
            return

        try:
            import shutil
            # Копируем проект в новую папку
            if os.path.exists(new_path):
                shutil.rmtree(new_path)
            shutil.copytree(self.current_project_path, new_path)

            # Открываем скопированный проект
            self.project_manager = ProjectManager(new_path)
            self.project_manager.load_project()

            self.current_project_path = new_path
            self.status_label.setText(f"Проект сохранён как: {os.path.basename(new_path)}")

        except Exception as e:
            ModernMessageBox.error(self, "Ошибка", f"Не удалось сохранить проект: {str(e)}")

    def close_project(self):
        """Закрытие проекта"""
        if not self.project_manager:
            return

        reply = ModernMessageBox.question(
            self, "Подтверждение",
            "Закрыть проект? Несохранённые изменения будут потеряны."
        )

        if reply:
            self.project_manager = None
            self.current_project_path = None
            self.current_designer = None

            # Очищаем вкладки
            self.tab_widget.clear()

            # Показываем стартовую страницу
            self.show_start_page()
            self.status_label.setText("Готов к работе")

    # ========== ОТКРЫТИЕ КОНСТРУКТОРОВ ==========

    def open_table_designer(self):
        """Открывает конструктор таблиц"""
        if not self.project_manager:
            ModernMessageBox.warning(self, "Предупреждение", "Сначала откройте проект")
            return

        # Проверяем, существует ли ещё tab_widget
        if not self.tab_widget or not self.tab_widget.isVisible():
            self.setup_ui()

        # Проверяем, не открыта ли уже вкладка с конструктором таблиц
        for i in range(self.tab_widget.count()):
            if self.tab_widget.tabText(i) == "📊 Конструктор таблиц":
                self.tab_widget.setCurrentIndex(i)
                return

        # Создаём конструктор таблиц
        designer = TableDesigner(self.project_manager)

        # Добавляем вкладку
        index = self.tab_widget.addTab(designer, "📊 Конструктор таблиц")
        self.tab_widget.setCurrentIndex(index)

        self.current_designer = designer
        self.status_label.setText("Конструктор таблиц открыт")

    def open_form_designer(self):
        """Открывает конструктор форм (заглушка)"""
        if not self.project_manager:
            ModernMessageBox.warning(self, "Предупреждение", "Сначала откройте проект")
            return

        ModernMessageBox.info(self, "Информация", "Конструктор форм находится в разработке")

    def open_report_designer(self):
        """Открывает конструктор отчётов (заглушка)"""
        if not self.project_manager:
            ModernMessageBox.warning(self, "Предупреждение", "Сначала откройте проект")
            return

        ModernMessageBox.info(self, "Информация", "Конструктор отчётов находится в разработке")

    def open_menu_designer(self):
        """Открывает конструктор меню (заглушка)"""
        if not self.project_manager:
            ModernMessageBox.warning(self, "Предупреждение", "Сначала откройте проект")
            return

        ModernMessageBox.info(self, "Информация", "Конструктор меню находится в разработке")

    def open_logic_designer(self):
        """Открывает конструктор логики (заглушка)"""
        if not self.project_manager:
            ModernMessageBox.warning(self, "Предупреждение", "Сначала откройте проект")
            return

        ModernMessageBox.info(self, "Информация", "Конструктор логики находится в разработке")

    def close_tab(self, index):
        """Закрывает вкладку"""
        if index >= 0 and index < self.tab_widget.count():
            widget = self.tab_widget.widget(index)
            self.tab_widget.removeTab(index)
            if widget:
                widget.deleteLater()

        if self.tab_widget.count() == 0:
            self.show_start_page()

    # ========== ДИАЛОГИ ==========

    def show_about(self):
        """Показывает информацию о программе"""
        ModernMessageBox.info(
            self,
            "О программе",
            "Low-Code Платформа\nВерсия 1.0\n\n"
            "Платформа для визуального создания приложений\n"
            "без написания кода.\n\n"
            "Конструкторы:\n"
            "• Таблиц\n"
            "• Форм\n"
            "• Отчётов\n"
            "• Меню\n"
            "• Логики"
        )

    def closeEvent(self, event):
        """Обработка закрытия окна"""
        if self.project_manager:
            reply = ModernMessageBox.question(
                self, "Подтверждение",
                "Закрыть программу? Несохранённые изменения будут потеряны."
            )
            if reply:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()