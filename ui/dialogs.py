"""
Диалоговые окна для работы с сотрудниками и отделами
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QFormLayout)
from PyQt6.QtCore import Qt
from database.models import Employee, Department
from database.database import Database
from typing import Optional

# Используем ModernEmployeeDialog как основной
from .modern_employee_dialog import ModernEmployeeDialog

# Создаем алиас для обратной совместимости
class AddEditEmployeeDialog(ModernEmployeeDialog):
    """
    Диалог для добавления/редактирования сотрудника
    Алиас для ModernEmployeeDialog
    """
    pass


class AddDepartmentDialog(QDialog):
    """
    Диалог для добавления нового отдела
    """
    def __init__(self, database: Database, parent=None):
        super().__init__(parent)
        self.database = database
        self.department_name = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('➕ Добавить отдел')
        self.setFixedSize(400, 180)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Заголовок
        title_label = QLabel('Создание нового отдела')
        title_label.setStyleSheet('''
            font-size: 14pt;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        ''')
        layout.addWidget(title_label)
        
        # Форма
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        name_label = QLabel('📁 Название отдела:')
        name_label.setStyleSheet('font-weight: 600; color: #34495e;')
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Введите название отдела...')
        self.name_input.setMinimumHeight(35)
        self.name_input.setStyleSheet('''
            QLineEdit {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 11pt;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #2196f3;
                background-color: #f8f9fa;
            }
        ''')
        
        form_layout.addRow(name_label, self.name_input)
        layout.addLayout(form_layout)
        
        layout.addStretch()
        
        # Кнопки
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        save_button = QPushButton('💾 Сохранить')
        save_button.setMinimumHeight(40)
        save_button.setCursor(Qt.CursorShape.PointingHandCursor)
        save_button.clicked.connect(self.save_department)
        save_button.setStyleSheet('''
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2196f3, stop:1 #1976d2);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 11pt;
                font-weight: 600;
                padding: 8px 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1976d2, stop:1 #1565c0);
            }
            QPushButton:pressed {
                background: #0d47a1;
            }
        ''')
        
        cancel_button = QPushButton('❌ Отмена')
        cancel_button.setMinimumHeight(40)
        cancel_button.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_button.clicked.connect(self.reject)
        cancel_button.setStyleSheet('''
            QPushButton {
                background-color: #757575;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 11pt;
                font-weight: 600;
                padding: 8px 20px;
            }
            QPushButton:hover {
                background-color: #616161;
            }
            QPushButton:pressed {
                background-color: #424242;
            }
        ''')
        
        button_layout.addWidget(save_button, 2)
        button_layout.addWidget(cancel_button, 1)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Стиль диалога
        self.setStyleSheet('''
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f5f7fa, stop:1 #e9ecef);
            }
        ''')
        
        # Фокус на поле ввода
        self.name_input.setFocus()
    
    def save_department(self):
        """Сохранение нового отдела"""
        name = self.name_input.text().strip()
        
        if not name:
            QMessageBox.warning(
                self,
                '⚠️ Ошибка',
                'Пожалуйста, введите название отдела!'
            )
            return
        
        # Проверка на существование отдела с таким именем
        existing_departments = self.database.get_all_departments()
        if any(dept.name.lower() == name.lower() for dept in existing_departments):
            QMessageBox.warning(
                self,
                '⚠️ Ошибка',
                f'Отдел "{name}" уже существует!'
            )
            return
        
        try:
            # Создаем новый отдел
            department = Department(name=name)
            self.database.add_department(department)
            self.department_name = name
            self.accept()
        except Exception as e:
            QMessageBox.critical(
                self,
                '❌ Ошибка',
                f'Не удалось создать отдел:\n{str(e)}'
            )

