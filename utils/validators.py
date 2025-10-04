import re
from typing import Tuple

class Validators:
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        if not email:
            return True, ""
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            return True, ""
        return False, "Неверный формат email"
    
    @staticmethod
    def validate_phone(phone: str) -> Tuple[bool, str]:
        if not phone:
            return True, ""
        
        phone_clean = re.sub(r'[^\d+]', '', phone)
        if len(phone_clean) >= 10:
            return True, ""
        return False, "Телефон должен содержать минимум 10 цифр"
    
    @staticmethod
    def validate_telegram(telegram: str) -> Tuple[bool, str]:
        if not telegram:
            return True, ""
        
        if telegram.startswith('@') and len(telegram) > 1:
            return True, ""
        return False, "Telegram должен начинаться с @"
    
    @staticmethod
    def validate_required(value: str, field_name: str) -> Tuple[bool, str]:
        if value and value.strip():
            return True, ""
        return False, f"Поле '{field_name}' обязательно для заполнения"
    
    @staticmethod
    def validate_date(date_str: str) -> Tuple[bool, str]:
        if not date_str:
            return True, ""
        
        pattern = r'^\d{4}-\d{2}-\d{2}$'
        if re.match(pattern, date_str):
            return True, ""
        return False, "Дата должна быть в формате YYYY-MM-DD"




