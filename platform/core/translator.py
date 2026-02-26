# -*- coding: utf-8 -*-

"""
Автоматический перевод с русского на английский
"""

import re
from typing import Dict


class Translator:
    """Класс для транслитерации и перевода"""
    
    TRANSLIT_DICT = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
        ' ': '_', '-': '_', '—': '_', '.': '_', ',': '_', '(': '', ')': ''
    }
    
    _cache: Dict[str, str] = {}
    
    @classmethod
    def to_english(cls, russian_text: str) -> str:
        if not russian_text:
            return ""
        
        if russian_text in cls._cache:
            return cls._cache[russian_text]
        
        text = russian_text.lower()
        
        result = ''
        for char in text:
            result += cls.TRANSLIT_DICT.get(char, char)
        
        while '__' in result:
            result = result.replace('__', '_')
        
        result = result.strip('_')
        
        if result and result[0].isdigit():
            result = 'f_' + result
        
        cls._cache[russian_text] = result
        return result
    
    @classmethod
    def clear_cache(cls):
        cls._cache.clear()