#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Точка входа в No-Code Platform
"""

import sys
import os

# Добавляем путь к папке platform
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from platform.main_window import MainWindow
from PyQt6.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Создаем нужные папки
    os.makedirs("projects", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()