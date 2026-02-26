# -*- coding: utf-8 -*-

"""
Управление проектами - ИСПРАВЛЕНО отображение списка
"""

import os
import json
import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field


@dataclass
class Project:
    """Класс проекта"""
    name: str
    description: str = ""
    author: str = ""
    created: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    modified: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    
    tables: List[Dict] = field(default_factory=list)
    forms: List[Dict] = field(default_factory=list)
    reports: List[Dict] = field(default_factory=list)
    menus: List[Dict] = field(default_factory=list)
    
    theme: str = "dark_blue"
    database_type: str = "sqlite"
    
    def to_dict(self) -> Dict:
        """Преобразовать в словарь для сохранения"""
        return {
            'name': self.name,
            'description': self.description,
            'author': self.author,
            'created': self.created,
            'modified': datetime.datetime.now().isoformat(),
            'theme': self.theme,
            'database_type': self.database_type,
            'tables': self.tables,
            'forms': self.forms,
            'reports': self.reports,
            'menus': self.menus,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Project':
        """Создать проект из словаря"""
        return cls(
            name=data.get('name', 'Без имени'),
            description=data.get('description', ''),
            author=data.get('author', ''),
            created=data.get('created', ''),
            modified=data.get('modified', ''),
            theme=data.get('theme', 'dark_blue'),
            database_type=data.get('database_type', 'sqlite'),
            tables=data.get('tables', []),
            forms=data.get('forms', []),
            reports=data.get('reports', []),
            menus=data.get('menus', [])
        )


class ProjectManager:
    """Менеджер проектов"""
    
    def __init__(self, projects_folder: str = "projects"):
        self.projects_folder = projects_folder
        self.current_project: Optional[Project] = None
        self.current_file: Optional[str] = None
        
        # Создаем папку для проектов, если её нет
        try:
            # Получаем абсолютный путь
            abs_path = os.path.abspath(projects_folder)
            os.makedirs(abs_path, exist_ok=True)
            print(f"✅ Папка проектов: {abs_path}")
            
            # Проверяем, есть ли там файлы
            if os.path.exists(abs_path):
                files = os.listdir(abs_path)
                print(f"📁 Файлы в папке: {files}")
        except Exception as e:
            print(f"❌ Ошибка создания папки: {e}")
    
    def create_project(self, name: str, description: str = "", author: str = "") -> Optional[Project]:
        """Создать новый проект"""
        try:
            self.current_project = Project(
                name=name,
                description=description,
                author=author
            )
            self.current_file = None
            print(f"✅ Проект '{name}' создан")
            return self.current_project
        except Exception as e:
            print(f"❌ Ошибка создания проекта: {e}")
            return None
    
    def save_project(self, filename: Optional[str] = None) -> bool:
        """Сохранить текущий проект"""
        if not self.current_project:
            print("❌ Нет текущего проекта для сохранения")
            return False
        
        try:
            if filename:
                self.current_file = filename
            elif not self.current_file:
                # Создаем имя файла из названия проекта
                safe_name = self.current_project.name.replace(' ', '_').lower()
                # Убираем недопустимые символы
                safe_name = ''.join(c for c in safe_name if c.isalnum() or c in '_-')
                self.current_file = os.path.join(
                    self.projects_folder, 
                    f"{safe_name}.ncp"
                )
            
            # Убеждаемся, что папка существует
            os.makedirs(os.path.dirname(self.current_file), exist_ok=True)
            
            data = self.current_project.to_dict()
            
            # Сохраняем с отступами для читаемости
            with open(self.current_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Проект сохранен: {self.current_file}")
            
            # Проверяем, что файл действительно создался
            if os.path.exists(self.current_file):
                print(f"📄 Файл создан, размер: {os.path.getsize(self.current_file)} байт")
            else:
                print(f"❌ Файл не создался!")
            
            return True
            
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def load_project(self, filename: str) -> Optional[Project]:
        """Загрузить проект из файла"""
        try:
            print(f"📂 Загрузка проекта: {filename}")
            
            if not os.path.exists(filename):
                print(f"❌ Файл не найден: {filename}")
                return None
            
            print(f"📄 Размер файла: {os.path.getsize(filename)} байт")
            
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"📊 Данные из файла: {list(data.keys())}")
            
            self.current_project = Project.from_dict(data)
            self.current_file = filename
            
            print(f"✅ Проект '{self.current_project.name}' загружен")
            return self.current_project
            
        except Exception as e:
            print(f"❌ Ошибка загрузки: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def list_projects(self) -> List[Dict]:
        """Получить список всех проектов"""
        projects = []
        
        try:
            # Получаем абсолютный путь
            abs_path = os.path.abspath(self.projects_folder)
            print(f"🔍 Поиск проектов в: {abs_path}")
            
            if not os.path.exists(abs_path):
                print(f"📁 Папка не найдена: {abs_path}")
                return projects
            
            # Смотрим все файлы в папке
            all_files = os.listdir(abs_path)
            print(f"📋 Все файлы в папке: {all_files}")
            
            # Ищем файлы с расширением .ncp
            ncp_files = [f for f in all_files if f.endswith('.ncp')]
            print(f"📋 NCP файлы: {ncp_files}")
            
            for file in ncp_files:
                filepath = os.path.join(abs_path, file)
                try:
                    print(f"📄 Чтение файла: {file}")
                    
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    project_info = {
                        'name': data.get('name', 'Без имени'),
                        'file': file,
                        'path': filepath,
                        'modified': data.get('modified', ''),
                        'description': data.get('description', '')
                    }
                    
                    projects.append(project_info)
                    print(f"✅ Найден проект: {project_info['name']}")
                    
                except json.JSONDecodeError as e:
                    print(f"⚠️ Ошибка JSON в {file}: {e}")
                except Exception as e:
                    print(f"⚠️ Ошибка чтения {file}: {e}")
                    continue
            
            print(f"📊 Всего проектов найдено: {len(projects)}")
            
        except Exception as e:
            print(f"❌ Ошибка списка проектов: {e}")
            import traceback
            traceback.print_exc()
        
        return projects