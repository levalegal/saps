import os
import shutil
from datetime import datetime
from typing import Optional
import json

class BackupManager:
    def __init__(self, db_path: str, backup_dir: str = 'backups'):
        self.db_path = db_path
        self.backup_dir = backup_dir
        self.settings_file = 'settings.json'
        
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
    
    def create_backup(self, comment: Optional[str] = None) -> str:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f'employees_backup_{timestamp}.db'
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        try:
            shutil.copy2(self.db_path, backup_path)
            
            if comment:
                info_file = backup_path + '.info'
                with open(info_file, 'w', encoding='utf-8') as f:
                    json.dump({
                        'timestamp': timestamp,
                        'comment': comment,
                        'size': os.path.getsize(backup_path)
                    }, f, ensure_ascii=False, indent=2)
            
            self.cleanup_old_backups()
            return backup_path
        except Exception as e:
            raise Exception(f'Ошибка создания резервной копии: {str(e)}')
    
    def restore_backup(self, backup_path: str) -> bool:
        try:
            if os.path.exists(backup_path):
                shutil.copy2(backup_path, self.db_path)
                return True
            return False
        except Exception as e:
            raise Exception(f'Ошибка восстановления: {str(e)}')
    
    def get_backups(self) -> list:
        backups = []
        if os.path.exists(self.backup_dir):
            for file in os.listdir(self.backup_dir):
                if file.endswith('.db'):
                    full_path = os.path.join(self.backup_dir, file)
                    info_path = full_path + '.info'
                    
                    backup_info = {
                        'name': file,
                        'path': full_path,
                        'size': os.path.getsize(full_path),
                        'date': datetime.fromtimestamp(os.path.getmtime(full_path)),
                        'comment': None
                    }
                    
                    if os.path.exists(info_path):
                        try:
                            with open(info_path, 'r', encoding='utf-8') as f:
                                info = json.load(f)
                                backup_info['comment'] = info.get('comment')
                        except:
                            pass
                    
                    backups.append(backup_info)
        
        return sorted(backups, key=lambda x: x['date'], reverse=True)
    
    def cleanup_old_backups(self, keep_count: int = 10):
        backups = self.get_backups()
        if len(backups) > keep_count:
            for backup in backups[keep_count:]:
                try:
                    os.remove(backup['path'])
                    info_path = backup['path'] + '.info'
                    if os.path.exists(info_path):
                        os.remove(info_path)
                except:
                    pass
    
    def delete_backup(self, backup_path: str):
        try:
            if os.path.exists(backup_path):
                os.remove(backup_path)
                info_path = backup_path + '.info'
                if os.path.exists(info_path):
                    os.remove(info_path)
                return True
            return False
        except Exception as e:
            raise Exception(f'Ошибка удаления резервной копии: {str(e)}')




