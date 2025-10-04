import json
import os
from typing import Any, Optional

class SettingsManager:
    def __init__(self, settings_file: str = 'settings.json'):
        self.settings_file = settings_file
        self.default_settings = {
            'cache_ttl': 300,
            'auto_backup': True,
            'backup_interval': 24,
            'max_backups': 10,
            'search_history_size': 10,
            'show_tooltips': True,
            'table_font_size': 10,
            'window_geometry': None,
            'recent_searches': []
        }
        self.settings = self.load_settings()
    
    def load_settings(self) -> dict:
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    return {**self.default_settings, **loaded}
            except:
                return self.default_settings.copy()
        return self.default_settings.copy()
    
    def save_settings(self):
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f'Ошибка сохранения настроек: {str(e)}')
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any):
        self.settings[key] = value
        self.save_settings()
    
    def add_search_to_history(self, search_query: str):
        if not search_query or not search_query.strip():
            return
        
        recent = self.settings.get('recent_searches', [])
        
        if search_query in recent:
            recent.remove(search_query)
        
        recent.insert(0, search_query)
        
        max_size = self.settings.get('search_history_size', 10)
        recent = recent[:max_size]
        
        self.settings['recent_searches'] = recent
        self.save_settings()
    
    def get_search_history(self) -> list:
        return self.settings.get('recent_searches', [])
    
    def clear_search_history(self):
        self.settings['recent_searches'] = []
        self.save_settings()
    
    def reset_to_defaults(self):
        self.settings = self.default_settings.copy()
        self.save_settings()




