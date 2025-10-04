from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                             QListWidget, QListWidgetItem, QLabel, QMessageBox,
                             QInputDialog)
from PyQt6.QtCore import Qt
from utils.backup_manager import BackupManager

class BackupDialog(QDialog):
    def __init__(self, backup_manager: BackupManager, parent=None):
        super().__init__(parent)
        self.backup_manager = backup_manager
        self.setWindowTitle('Управление резервными копиями')
        self.setMinimumSize(600, 400)
        self.init_ui()
        self.load_backups()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        info_label = QLabel('Резервные копии базы данных:')
        layout.addWidget(info_label)
        
        self.backup_list = QListWidget()
        self.backup_list.itemDoubleClicked.connect(self.show_backup_info)
        layout.addWidget(self.backup_list)
        
        button_layout = QHBoxLayout()
        
        create_btn = QPushButton('Создать копию')
        create_btn.clicked.connect(self.create_backup)
        button_layout.addWidget(create_btn)
        
        restore_btn = QPushButton('Восстановить')
        restore_btn.clicked.connect(self.restore_backup)
        button_layout.addWidget(restore_btn)
        
        delete_btn = QPushButton('Удалить')
        delete_btn.clicked.connect(self.delete_backup)
        button_layout.addWidget(delete_btn)
        
        button_layout.addStretch()
        
        close_btn = QPushButton('Закрыть')
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def load_backups(self):
        self.backup_list.clear()
        backups = self.backup_manager.get_backups()
        
        for backup in backups:
            date_str = backup['date'].strftime('%Y-%m-%d %H:%M:%S')
            size_mb = backup['size'] / (1024 * 1024)
            
            text = f"{date_str} ({size_mb:.2f} MB)"
            if backup['comment']:
                text += f" - {backup['comment']}"
            
            item = QListWidgetItem(text)
            item.setData(Qt.ItemDataRole.UserRole, backup)
            self.backup_list.addItem(item)
        
        if not backups:
            item = QListWidgetItem('Нет резервных копий')
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.backup_list.addItem(item)
    
    def create_backup(self):
        comment, ok = QInputDialog.getText(
            self,
            'Создание резервной копии',
            'Комментарий (необязательно):'
        )
        
        if ok:
            try:
                backup_path = self.backup_manager.create_backup(
                    comment if comment.strip() else None
                )
                QMessageBox.information(
                    self,
                    'Успех',
                    f'Резервная копия создана:\n{backup_path}'
                )
                self.load_backups()
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', str(e))
    
    def restore_backup(self):
        current_item = self.backup_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, 'Ошибка', 'Выберите резервную копию!')
            return
        
        backup = current_item.data(Qt.ItemDataRole.UserRole)
        if not backup:
            return
        
        reply = QMessageBox.question(
            self,
            'Подтверждение',
            f'Восстановить базу данных из копии?\n\n'
            f'Дата: {backup["date"].strftime("%Y-%m-%d %H:%M:%S")}\n\n'
            f'⚠️ ВНИМАНИЕ: Текущие данные будут заменены!\n'
            f'Рекомендуется создать резервную копию текущего состояния.',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.backup_manager.restore_backup(backup['path'])
                QMessageBox.information(
                    self,
                    'Успех',
                    'База данных восстановлена!\nПерезапустите приложение для применения изменений.'
                )
                self.accept()
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', str(e))
    
    def delete_backup(self):
        current_item = self.backup_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, 'Ошибка', 'Выберите резервную копию!')
            return
        
        backup = current_item.data(Qt.ItemDataRole.UserRole)
        if not backup:
            return
        
        reply = QMessageBox.question(
            self,
            'Подтверждение',
            f'Удалить резервную копию?\n\n{backup["name"]}',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.backup_manager.delete_backup(backup['path'])
                QMessageBox.information(self, 'Успех', 'Резервная копия удалена!')
                self.load_backups()
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', str(e))
    
    def show_backup_info(self, item):
        backup = item.data(Qt.ItemDataRole.UserRole)
        if not backup:
            return
        
        info = f"Имя файла: {backup['name']}\n"
        info += f"Дата: {backup['date'].strftime('%Y-%m-%d %H:%M:%S')}\n"
        info += f"Размер: {backup['size'] / (1024 * 1024):.2f} MB\n"
        if backup['comment']:
            info += f"Комментарий: {backup['comment']}\n"
        info += f"Путь: {backup['path']}"
        
        QMessageBox.information(self, 'Информация о копии', info)




