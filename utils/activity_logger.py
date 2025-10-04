import logging
import os
from datetime import datetime
from typing import Optional
import json

class ActivityLogger:
    def __init__(self, log_dir='logs', log_file='activity.log', history_file='history.json'):
        self.log_dir = log_dir
        self.log_file = os.path.join(log_dir, log_file)
        self.history_file = os.path.join(log_dir, history_file)
        
        os.makedirs(log_dir, exist_ok=True)
        
        self.logger = logging.getLogger('EmployeeDirectory')
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
            file_handler.setLevel(logging.INFO)
            
            formatter = logging.Formatter(
                '%(asctime)s | %(levelname)s | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(formatter)
            
            self.logger.addHandler(file_handler)
    
    def log_action(self, action: str, entity_type: str, entity_id: Optional[int], 
                   user: str, details: Optional[str] = None):
        message = f"{action} | {entity_type} | ID:{entity_id} | User:{user}"
        if details:
            message += f" | {details}"
        
        self.logger.info(message)
        
        self.add_to_history(action, entity_type, entity_id, user, details)
    
    def add_to_history(self, action: str, entity_type: str, entity_id: Optional[int],
                       user: str, details: Optional[str] = None):
        history = self.load_history()
        
        entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'entity_type': entity_type,
            'entity_id': entity_id,
            'user': user,
            'details': details
        }
        
        history.insert(0, entry)
        
        if len(history) > 1000:
            history = history[:1000]
        
        self.save_history(history)
    
    def load_history(self) -> list:
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_history(self, history: list):
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    
    def get_recent_history(self, limit: int = 50) -> list:
        history = self.load_history()
        return history[:limit]
    
    def get_entity_history(self, entity_type: str, entity_id: int) -> list:
        history = self.load_history()
        return [h for h in history if h['entity_type'] == entity_type and h['entity_id'] == entity_id]
    
    def get_user_activity(self, user: str) -> list:
        history = self.load_history()
        return [h for h in history if h['user'] == user]
    
    def log_employee_added(self, employee_id: int, user: str, employee_name: str):
        self.log_action('ДОБАВЛЕН', 'Сотрудник', employee_id, user, employee_name)
    
    def log_employee_updated(self, employee_id: int, user: str, employee_name: str):
        self.log_action('ОБНОВЛЕН', 'Сотрудник', employee_id, user, employee_name)
    
    def log_employee_deleted(self, employee_id: int, user: str, employee_name: str):
        self.log_action('УДАЛЕН', 'Сотрудник', employee_id, user, employee_name)
    
    def log_department_added(self, dept_id: int, user: str, dept_name: str):
        self.log_action('ДОБАВЛЕН', 'Отдел', dept_id, user, dept_name)
    
    def log_export(self, user: str, export_type: str, count: int):
        self.log_action('ЭКСПОРТ', export_type, None, user, f'Записей: {count}')
    
    def log_import(self, user: str, import_type: str, count: int):
        self.log_action('ИМПОРТ', import_type, None, user, f'Записей: {count}')
    
    def log_login(self, user: str):
        self.log_action('ВХОД', 'Система', None, user, 'Успешная авторизация')
    
    def log_search(self, user: str, query: str, results_count: int):
        self.log_action('ПОИСК', 'Сотрудники', None, user, f'Запрос: {query}, Найдено: {results_count}')



