# -*- coding: utf-8 -*-

"""
Управление проектами
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
        return cls(
            name=data['name'],
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
        
        os.makedirs(projects_folder, exist_ok=True)
    
    def create_project(self, name: str, description: str = "", author: str = "") -> Project:
        self.current_project = Project(
            name=name,
            description=description,
            author=author
        )
        self.current_file = None
        return self.current_project
    
    def save_project(self, filename: Optional[str] = None) -> bool:
        if not self.current_project:
            return False
        
        if filename:
            self.current_file = filename
        elif not self.current_file:
            safe_name = self.current_project.name.replace(' ', '_').lower()
            self.current_file = os.path.join(
                self.projects_folder, 
                f"{safe_name}.ncp"
            )
        
        try:
            data = self.current_project.to_dict()
            with open(self.current_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
            return False
    
    def load_project(self, filename: str) -> Optional[Project]:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.current_project = Project.from_dict(data)
            self.current_file = filename
            return self.current_project
        except Exception as e:
            print(f"Ошибка загрузки: {e}")
            return None
    
    def list_projects(self) -> List[Dict]:
        projects = []
        
        if not os.path.exists(self.projects_folder):
            return projects
        
        for file in os.listdir(self.projects_folder):
            if file.endswith('.ncp'):
                filepath = os.path.join(self.projects_folder, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    projects.append({
                        'name': data.get('name', 'Без имени'),
                        'file': file,
                        'path': filepath,
                        'modified': data.get('modified', ''),
                        'description': data.get('description', '')
                    })
                except:
                    continue
        
        return projects