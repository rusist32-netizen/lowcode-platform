#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Запуск с максимальной отладкой
"""

import sys
import os
import traceback

# Добавляем путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Перехватываем все исключения
def excepthook(exc_type, exc_value, exc_traceback):
    print("=" * 60)
    print("❌ НЕПЕРЕХВАЧЕННОЕ ИСКЛЮЧЕНИЕ!")
    print("=" * 60)
    print(f"Тип: {exc_type}")
    print(f"Значение: {exc_value}")
    print("\nTraceback:")
    traceback.print_tb(exc_traceback)
    print("=" * 60)
    
    # Сохраняем в файл
    with open("fatal_error.txt", "w", encoding="utf-8") as f:
        f.write(f"Тип: {exc_type}\n")
        f.write(f"Значение: {exc_value}\n\n")
        f.write("Traceback:\n")
        traceback.print_tb(exc_traceback, file=f)
    
    input("\nНажмите Enter для выхода...")

sys.excepthook = excepthook

try:
    print("=" * 60)
    print("🚀 ЗАПУСК С ОТЛАДКОЙ")
    print("=" * 60)
    
    from platform.main_window import MainWindow
    from PyQt6.QtWidgets import QApplication
    
    print("✅ Импорты успешны")
    
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    print("✅ Приложение создано")
    
    # Проверяем папки
    os.makedirs("projects", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    
    print(f"📁 Папка проектов: {os.path.abspath('projects')}")
    
    # Проверяем файлы проектов
    if os.path.exists("projects"):
        files = os.listdir("projects")
        print(f"📋 Файлы в projects: {files}")
    
    window = MainWindow()
    window.show()
    
    print("✅ Окно показано")
    
    sys.exit(app.exec())
    
except Exception as e:
    print("=" * 60)
    print("❌ ОШИБКА ЗАПУСКА!")
    print("=" * 60)
    print(f"Ошибка: {e}")
    print("\nПодробности:")
    traceback.print_exc()
    
    with open("startup_error.txt", "w", encoding="utf-8") as f:
        f.write(f"Ошибка: {e}\n\n")
        traceback.print_exc(file=f)
    
    input("\nНажмите Enter для выхода...")