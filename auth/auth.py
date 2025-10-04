import hashlib
from typing import Optional
from database.database import Database
from database.models import User

class AuthManager:
    def __init__(self, database: Database):
        self.database = database
        self.current_user: Optional[User] = None
    
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate(self, username: str, password: str) -> bool:
        user = self.database.get_user(username)
        
        if user and user.password_hash == self.hash_password(password):
            self.current_user = user
            return True
        return False
    
    def logout(self):
        self.current_user = None
    
    def is_authenticated(self) -> bool:
        return self.current_user is not None
    
    def has_permission(self, permission: str) -> bool:
        if not self.current_user:
            return False
        
        role = self.current_user.role
        
        if role == 'admin':
            return True
        elif role == 'editor':
            return permission in ['view', 'add', 'edit']
        elif role == 'user':
            return permission == 'view'
        
        return False
    
    def get_current_user(self) -> Optional[User]:
        return self.current_user
    
    def initialize_default_users(self):
        try:
            if not self.database.get_user('admin'):
                admin_user = User(
                    id=None,
                    username='admin',
                    password_hash=self.hash_password('admin123'),
                    role='admin',
                    employee_id=None
                )
                self.database.add_user(admin_user)
            
            if not self.database.get_user('editor'):
                editor_user = User(
                    id=None,
                    username='editor',
                    password_hash=self.hash_password('editor123'),
                    role='editor',
                    employee_id=None
                )
                self.database.add_user(editor_user)
            
            if not self.database.get_user('user'):
                user_user = User(
                    id=None,
                    username='user',
                    password_hash=self.hash_password('user123'),
                    role='user',
                    employee_id=None
                )
                self.database.add_user(user_user)
        except Exception:
            pass



